#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, json, sys, itertools
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

def rpc(url, method, params, auth=None, token=None, req_id=1):
    payload = {"jsonrpc":"2.0","method":method,"params":params or {}, "id":req_id}
    if auth: payload["auth"] = auth
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type":"application/json-rpc"}
    if token: headers["Authorization"] = f"Bearer {token}"
    try:
        resp = urlopen(Request(url, data=data, headers=headers))
        body = resp.read().decode("utf-8")
        js = json.loads(body)
        if "error" in js: raise RuntimeError(f"API error on {method}: {js['error']}")
        return js.get("result")
    except HTTPError as e:
        raise RuntimeError(f"HTTPError {e.code} on {method}: {e.read().decode('utf-8','ignore')}")
    except URLError as e:
        raise RuntimeError(f"URLError on {method}: {e}")

def login(url, user, password):
    return rpc(url, "user.login", {"user": user, "password": password})

def get_prototypes(url, auth, token, templateid, discoveryid):
    # pega TODOS os prototypes do template + LLD
    params = {
        "hostids": [str(templateid)],
        "discoveryids": [str(discoveryid)],
        "output": ["triggerid","name","description"],
        "expandDescription": True
    }
    return rpc(url, "triggerprototype.get", params, auth=auth, token=token) or []

def delete_prototypes(url, auth, token, ids):
    total = 0
    for i in range(0, len(ids), 200):
        batch = ids[i:i+200]
        res = rpc(url, "triggerprototype.delete", batch, auth=auth, token=token)
        total += len(res) if isinstance(res, list) else 0
    return total

def main():
    ap = argparse.ArgumentParser(description="Deleta APENAS trigger prototypes (LLD) por templateid+discoveryid, filtrando por texto.")
    ap.add_argument("--url", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--token")
    g.add_argument("--user")
    ap.add_argument("--password", help="Obrigatória se usar --user")
    ap.add_argument("--templateid", required=True)
    ap.add_argument("--discoveryid", required=True)
    ap.add_argument("--match", default="Menor do que 60 dias", help="Texto a casar (case-insensitive)")
    ap.add_argument("--dry-run", action="store_true", help="Só lista; não deleta")
    ap.add_argument("--yes", action="store_true", help="Pula confirmação")
    args = ap.parse_args()

    if args.user and not args.password:
        ap.error("--password é obrigatório quando usar --user")

    auth = None
    if not args.token:
        auth = login(args.url, args.user, args.password)

    # 1) Buscar todos os prototypes do template+LLD
    protos = get_prototypes(args.url, auth, args.token, args.templateid, args.discoveryid)

    # 2) Filtrar por texto (name+description), case-insensitive
    needle = (args.match or "").lower()
    protos = [p for p in protos if needle in ((p.get("name") or "") + " " + (p.get("description") or "")).lower()]

    print(f"Foram encontradas {len(protos)} trigger prototypes com o nome especificado ('{args.match}').")
    if not protos:
        print("Nada a fazer.")
        return 0

    for p in protos:
        pname = p.get("name") or p.get("description") or "(sem nome)"
        print(f"  [PROTO] {p.get('triggerid')} - {pname}")

    if args.dry_run:
        print("\n[DRY-RUN] Nenhum prototype será deletado.")
        return 0

    if not args.yes:
        confirm = input("\nForam encontradas {} triggers com o nome especificado, tem certeza que gostaria de deletar? Digite YES para confirmar: ".format(len(protos)))
        if confirm.strip() != "YES":
            print("Operação abortada.")
            return 1

    # 3) Deletar SOMENTE os prototypes encontrados
    proto_ids = [p["triggerid"] for p in protos]
    deleted = delete_prototypes(args.url, auth, args.token, proto_ids)
    print(f">> Prototypes deletados: {deleted}")
    print("Concluído.")

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"ERRO: {e}", file=sys.stderr)
        sys.exit(2)