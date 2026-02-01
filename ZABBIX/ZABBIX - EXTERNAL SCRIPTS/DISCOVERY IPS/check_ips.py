import requests
import json
import os
import subprocess
import urllib3

# === CONFIGS ===
ZABBIX_URL = "http://[IP_ADDRESS]/zabbix/api_jsonrpc.php"
ZABBIX_TOKEN = "TOKEN"
ZABBIX_HOST = "Network Discovery Monitor"
TRAPPER_KEY = "undiscovered.ips"
CACHE_FILE = "/tmp/zbx_ip_cache.json"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# === HEADERS ===
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ZABBIX_TOKEN}"
}

# === API CALL ===
def zabbix_api(method, params):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "auth": ZABBIX_TOKEN,
        "id": 1
    }
    res = requests.post(ZABBIX_URL, headers=HEADERS, json=payload, verify=False)
    res.raise_for_status()
    return res.json().get("result", [])

# === GET IPs DA DISCOVERY ===
def get_discovered_ips():
    discovered_ips = set()
    drules = zabbix_api("discoveryrule.get", {"output": "extend"})
    for drule in drules:
        dresults = zabbix_api("discovery.get", {"druleids": drule["druleid"], "output": "extend"})
        for result in dresults:
            if result.get("ip") and result.get("status") == "0":
                discovered_ips.add(result["ip"])
    return discovered_ips

# === VERIFICAR SE IP TEM HOST ===
def ip_has_host(ip):
    result = zabbix_api("hostinterface.get", {"filter": {"ip": ip}})
    return len(result) > 0

# === CACHE ===
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            return set(json.load(f))
    return set()

def save_cache(ips):
    with open(CACHE_FILE, "w") as f:
        json.dump(list(ips), f)

# === ENVIAR PRO TRAPPER ===
def send_to_trapper(ips):
    if not ips:
        return
    data = "\\n".join(ips)
    cmd = [
        "zabbix_sender",
        "-z", "127.0.0.1",
        "-s", ZABBIX_HOST,
        "-k", TRAPPER_KEY,
        "-o", data
    ]
    subprocess.run(cmd, check=True)

# === MAIN ===
def main():
    current_ips = get_discovered_ips()
    cached_ips = load_cache()

    new_ips = current_ips - cached_ips
    ips_sem_host = [ip for ip in new_ips if not ip_has_host(ip)]

    if ips_sem_host:
        print(f"[!] IPs novos sem host: {ips_sem_host}")
        send_to_trapper(ips_sem_host)
    else:
        print("[✓] Nenhum IP novo sem host.")

    save_cache(current_ips)

if __name__ == "__main__":
    main()
