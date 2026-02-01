from flask import Flask, render_template_string
import subprocess
import time
import threading
import sqlite3
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List
from datetime import datetime

# e-mail
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

app = Flask(__name__)

# ============================ CONFIG: ============================ #
BASE = "/opt/scripts/dynatrace/psc"

APIS = {
    "ApiAdmin": {
        "falha": f"{BASE}/FALHAS/get-apiadmin-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-apiadmin-degradation.sh",
    },
    "AplicativoMovel": {
        "falha": f"{BASE}/FALHAS/get-aplicativomovel-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-aplicativomovel-degradation.sh",
    },
    "Authentication": {
        "falha": f"{BASE}/FALHAS/get-authentication-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-authentication-degradation.sh",
    },
    "Autorizacoes": {
        "falha": f"{BASE}/FALHAS/get-autorizacoes-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-autorizacoes-degradation.sh",
    },
    "CAPSC-Portal": {
        "falha": f"{BASE}/FALHAS/get-capsc-portal-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-capsc-portal-degradation.sh",
    },
    "CAPSC": {
        "falha": f"{BASE}/FALHAS/get-capsc-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-capsc-degradation.sh",
    },
    "CAPSC-WS": {
        "falha": f"{BASE}/FALHAS/get-capsc-ws-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-capsc-ws-degradation.sh",
    },
    "Certificate": {
        "falha": f"{BASE}/FALHAS/get-certificate-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-certificate-degradation.sh",
    },
    "CertificateUse": {
        "falha": f"{BASE}/FALHAS/get-certificateuse-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-certificateuse-degradation.sh",
    },
    "Demonstracao": {
        "falha": f"{BASE}/FALHAS/get-demonstracao-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-demonstracao-degradation.sh",
    },
    "Desktop-OAuth": {
        "falha": f"{BASE}/FALHAS/get-desktop-oauth-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-desktop-oauth-degradation.sh",
    },
    "Desktop": {
        "falha": f"{BASE}/FALHAS/get-desktop-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-desktop-degradation.sh",
    },
    "Device": {
        "falha": f"{BASE}/FALHAS/get-device-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-device-degradation.sh",
    },
    "Docs": {
        "falha": f"{BASE}/FALHAS/get-docs-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-docs-degradation.sh",
    },
    "GedarAuthentication": {
        "falha": f"{BASE}/FALHAS/get-gedarauthentication-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-gedarauthentication-degradation.sh",
    },
    "History": {
        "falha": f"{BASE}/FALHAS/get-history-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-history-degradation.sh",
    },
    "HSM": {
        "falha": f"{BASE}/FALHAS/get-hsm-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-hsm-degradation.sh",
    },
    "IntegracoesPSC": {
        "falha": f"{BASE}/FALHAS/get-integracoespsc-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-integracoespsc-degradation.sh",
    },
    "Mensagens": {
        "falha": f"{BASE}/FALHAS/get-mensagens-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-mensagens-degradation.sh",
    },
    "OAuth": {
        "falha": f"{BASE}/FALHAS/get-oauth-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-oauth-degradation.sh",
    },
    "Portal": {
        "falha": f"{BASE}/FALHAS/get-portal-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-portal-degradation.sh",
    },
    "ProvedoresPSC": {
        "falha": f"{BASE}/FALHAS/get-provedorespsc-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-provedorespsc-degradation.sh",
    },
    "PSC": {
        "falha": f"{BASE}/FALHAS/get-psc-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-psc-degradation.sh",
    },
    "PushNotification": {
        "falha": f"{BASE}/FALHAS/get-pushnotification-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-pushnotification-degradation.sh",
    },
    "Release": {
        "falha": f"{BASE}/FALHAS/get-release-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-release-degradation.sh",
    },
    "Signature": {
        "falha": f"{BASE}/FALHAS/get-signature-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-signature-degradation.sh",
    },
    "TSP": {
        "falha": f"{BASE}/FALHAS/get-tsp-problem.sh",
        "degrad": f"{BASE}/LENTIDAO/get-tsp-degradation.sh",
    },
}

INTERVAL_SEC = 180
TIMEOUT_SEC = 20

DB_PATH = f"{BASE}/status-page/status_history.sqlite"

# ============================ E-MAIL ============================ #
# Ajuste aqui
SMTP_HOST = "smtp.seudominio.local"
SMTP_PORT = 587
SMTP_USER = "usuario@seudominio.local"
SMTP_PASS = "SENHA_AQUI"

MAIL_FROM = "safeid-monitor@seudominio.local"
MAIL_TO = ["destino1@seudominio.local"]
MAIL_SUBJECT = "DISPONIBILIDADE SERVIÇOS SAFEID"
SMTP_USE_STARTTLS = True  # se seu SMTP não usar TLS, coloque False
# =============================================================== #
# ================================================================== #

@dataclass
class ApiState:
    falha: Optional[int] = None
    degrad: Optional[int] = None
    updated_at: float = 0.0
    error: Optional[str] = None

    # contadores do dia (reset meia-noite)
    daily_falha: int = 0
    daily_degrad: int = 0
    day_key: str = ""  # YYYY-MM-DD

STATE: Dict[str, ApiState] = {name: ApiState() for name in APIS.keys()}
LOCK = threading.Lock()

# =========================== FRONT-END (OPMON STYLE) ============================= #
HTML = """
<!doctype html>
<html lang="pt-br">
<head>
  <meta charset="utf-8">
  {% if refresh_sec and refresh_sec > 0 %}
  <meta http-equiv="refresh" content="{{refresh_sec}}">
  {% endif %}
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DISPONIBILIDADE SERVIÇOS SAFEID</title>

  <style>
    :root{
      --greenTop:#0aa35b;
      --greenTop2:#078a4d;
      --panelGreen:#11a560;
      --panelGreen2:#0f8f55;
      --border:#0b7a48;

      --bg:#e9ecef;
      --card:#ffffff;

      --ok:#1db954;
      --alert:#f1c40f;
      --crit:#e74c3c;
      --both:#8e44ad;
      --unk:#7f8c8d;

      --text:#1f2937;
    }

    *{ box-sizing: border-box; }
    body{
      margin:0;
      font-family: Arial, Helvetica, sans-serif;
      background: var(--bg);
      color: var(--text);
    }

    .topbar{
      background: linear-gradient(180deg, var(--greenTop), var(--greenTop2));
      color: #fff;
      padding: 14px 16px;
      border-bottom: 4px solid #0a6f43;
    }
    .topbar-inner{
      max-width: 1920px;
      margin: 0 auto;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap: 16px;
    }
    .title{
      flex:1;
      text-align:center;
      font-weight: 900;
      letter-spacing: 1px;
      text-transform: uppercase;
      font-size: 26px;
      line-height: 1;
      white-space: nowrap;
    }
    .updated{
      font-weight: 800;
      font-size: 12px;
      text-transform: uppercase;
      opacity: .95;
      white-space: nowrap;
      text-align:right;
    }

    .wrap{
      max-width: 1920px;
      margin: 0 auto;
      padding: 12px;
    }

    /* gráficos em cima */
    .grid2{
      display:grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      align-items: stretch;
      margin-bottom: 12px;
    }

    /* tabelas embaixo */
    .grid2tables{
      display:grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      align-items: start;
    }

    .panel{
      background: var(--card);
      border: 2px solid var(--border);
      box-shadow: 0 1px 0 rgba(0,0,0,.04);
    }

    .panel-head{
      background: linear-gradient(180deg, var(--panelGreen), var(--panelGreen2));
      color:#fff;
      font-weight: 900;
      letter-spacing: .8px;
      text-transform: uppercase;
      padding: 10px 12px;
      border-bottom: 2px solid var(--border);
      text-align:center;
      font-size: 18px;
    }

    table{
      width:100%;
      border-collapse: collapse;
      table-layout: fixed;
    }
    thead th{
      background:#e5efe9;
      color:#0b3a22;
      font-weight: 900;
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: .7px;
      padding: 8px 8px;
      border-bottom: 1px solid rgba(0,0,0,.12);
      text-align:left;
      white-space: nowrap;
    }
    tbody td{
      padding: 8px 8px;
      border-top: 1px solid rgba(0,0,0,.08);
      font-size: 12px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      vertical-align: middle;
    }
    tbody tr:nth-child(odd){ background:#ffffff; }
    tbody tr:nth-child(even){ background:#f7fbf9; }

    .right{ text-align:right; }

    .dot{
      width: 10px; height: 10px;
      border-radius: 50%;
      display:inline-block;
      margin-right: 8px;
      vertical-align: middle;
      box-shadow: 0 0 0 2px rgba(0,0,0,.08);
    }
    .ok{ background: var(--ok); }
    .alert{ background: var(--alert); }
    .crit{ background: var(--crit); }
    .both{ background: var(--both); }
    .unk{ background: var(--unk); }

    .kpi{
      background: var(--card);
      border: 2px solid var(--border);
      padding: 10px 12px;
      display:grid;
      grid-template-columns: 220px 1fr;
      gap: 12px;
      align-items:center;
      min-height: 170px;
    }
    .kpi-title{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap: 10px;
      margin-bottom: 8px;
    }
    .kpi-title .name{
      background: linear-gradient(180deg, var(--panelGreen), var(--panelGreen2));
      color:#fff;
      font-weight: 900;
      letter-spacing: .8px;
      text-transform: uppercase;
      padding: 10px 12px;
      border-radius: 4px;
      min-width: 130px;
      text-align:center;
      border: 2px solid var(--border);
    }
    .kpi-title .total{
      font-weight: 900;
      font-size: 22px;
      padding: 8px 10px;
      border: 2px solid rgba(0,0,0,.12);
      border-radius: 4px;
      background:#fff;
      min-width: 90px;
      text-align:center;
    }

    .donut{
      width: 110px; height: 110px;
      border-radius: 50%;
      background: conic-gradient(var(--ok) calc(var(--p) * 1%), #e6e6e6 0);
      position: relative;
      margin: 0 auto;
    }
    .donut::after{
      content:"";
      position:absolute;
      inset: 16px;
      background: #fff;
      border-radius: 50%;
      box-shadow: inset 0 0 0 2px rgba(0,0,0,.06);
    }
    .donut-label{
      position:absolute;
      inset:0;
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight: 900;
      z-index: 1;
      font-size: 18px;
    }
    .incidents{
      text-align:center;
      font-weight: 900;
      color: var(--crit);
      text-transform: uppercase;
      margin-top: 8px;
      letter-spacing: .6px;
    }
    .incidents .n{
      display:block;
      font-size: 22px;
      margin-top: 4px;
    }

    .bars{
      display:flex;
      align-items:flex-end;
      gap: 10px;
      height: 120px;
      padding: 0 6px;
      border-left: 2px solid rgba(0,0,0,.12);
      border-bottom: 2px solid rgba(0,0,0,.12);
    }
    .bar{
      width: 44px;
      border-radius: 4px 4px 0 0;
      position: relative;
      box-shadow: inset 0 0 0 1px rgba(0,0,0,.10);
    }
    .bar span{
      position:absolute;
      top: -18px;
      left: 50%;
      transform: translateX(-50%);
      font-weight: 900;
      font-size: 11px;
      white-space: nowrap;
    }
    .bar small{
      position:absolute;
      bottom: -20px;
      left: 50%;
      transform: translateX(-50%);
      font-weight: 900;
      font-size: 10px;
      text-transform: uppercase;
      opacity: .85;
    }

    .bar-ok{ background: var(--ok); }
    .bar-al{ background: var(--alert); }
    .bar-cr{ background: var(--crit); }
    .bar-bo{ background: var(--both); }
    .bar-un{ background: var(--unk); }

    @media (max-width: 1300px){
      .grid2{ grid-template-columns: 1fr; }
      .grid2tables{ grid-template-columns: 1fr; }
      .kpi{ grid-template-columns: 1fr; }
    }
  </style>
</head>

<body>
  <div class="topbar">
    <div class="topbar-inner">
      <div class="title">DISPONIBILIDADE SERVIÇOS SAFEID</div>
      <div class="updated">
        ÚLTIMA ATUALIZAÇÃO<br>
        {{summary.updated_at}}
      </div>
    </div>
  </div>

  <div class="wrap">

    <!-- KPIs / gráficos EM CIMA -->
    <div class="grid2">
      <div class="kpi">
        <div>
          <div class="kpi-title">
            <div class="name">SERVIÇOS</div>
            <div class="total">{{summary.total}}</div>
          </div>
          <div class="donut" style="--p: {{summary.ok_pct}};">
            <div class="donut-label">{{summary.ok_pct}}%</div>
          </div>
          <div class="incidents">
            INCIDENTES
            <span class="n">{{summary.incidents}}</span>
          </div>
        </div>

        <div>
          <div class="bars" aria-label="Distribuição por status">
            <div class="bar bar-bo" style="height: {{summary.bar_purple}}%;">
              <span>{{summary.purple}}</span><small>fal+deg</small>
            </div>
            <div class="bar bar-cr" style="height: {{summary.bar_red}}%;">
              <span>{{summary.red}}</span><small>falha</small>
            </div>
            <div class="bar bar-al" style="height: {{summary.bar_yellow}}%;">
              <span>{{summary.yellow}}</span><small>alerta</small>
            </div>
            <div class="bar bar-un" style="height: {{summary.bar_gray}}%;">
              <span>{{summary.unknown}}</span><small>indef</small>
            </div>
            <div class="bar bar-ok" style="height: {{summary.bar_green}}%;">
              <span>{{summary.ok}}</span><small>ok</small>
            </div>
          </div>
        </div>
      </div>

      <div class="kpi">
        <div>
          <div class="kpi-title">
            <div class="name">APLICAÇÕES</div>
            <div class="total">{{summary.total}}</div>
          </div>
          <div class="donut" style="--p: {{summary.ok_pct}};">
            <div class="donut-label">{{summary.ok_pct}}%</div>
          </div>
          <div class="incidents">
            INCIDENTES
            <span class="n">{{summary.incidents}}</span>
          </div>
        </div>

        <div>
          <div class="bars">
            <div class="bar bar-cr" style="height: {{summary.bar_red_plus_purple}}%;">
              <span>{{summary.red_plus_purple}}</span><small>crítico</small>
            </div>
            <div class="bar bar-al" style="height: {{summary.bar_yellow}}%;">
              <span>{{summary.yellow}}</span><small>alerta</small>
            </div>
            <div class="bar bar-ok" style="height: {{summary.bar_green}}%;">
              <span>{{summary.ok}}</span><small>ok</small>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabelas EM BAIXO (sem HOSTS) -->
    <div class="grid2tables">

      <!-- SERVIÇOS -->
      <div class="panel">
        <div class="panel-head">SERVIÇOS</div>
        <table>
          <thead>
            <tr>
              <th style="width:52%">GRUPO</th>
              <th class="right" style="width:16%">RECURSOS</th>
              <th class="right" style="width:10%">OK</th>
              <th class="right" style="width:11%">ALERTA</th>
              <th class="right" style="width:11%">CRÍTICO</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td title="Degradação (yellow) + Falha+Degradação (purple)"><span class="dot alert"></span>DEGRADAÇÃO</td>
              <td class="right">{{summary.total}}</td>
              <td class="right">{{summary.ok}}</td>
              <td class="right">{{summary.yellow}}</td>
              <td class="right">{{summary.red_plus_purple}}</td>
            </tr>
            <tr>
              <td title="Erros de coleta/script/timeout"><span class="dot unk"></span>INDISPONÍVEL</td>
              <td class="right">{{summary.total}}</td>
              <td class="right">{{summary.total - summary.unknown}}</td>
              <td class="right">0</td>
              <td class="right">{{summary.unknown}}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- APLICAÇÕES -->
      <div class="panel">
        <div class="panel-head">APLICAÇÕES</div>
        <table>
          <thead>
            <tr>
              <th style="width:58%">GRUPO</th>
              <th class="right" style="width:14%">FALHA</th>
              <th class="right" style="width:14%">DEGRAD</th>
              <th class="right" style="width:14%">UPD</th>
            </tr>
          </thead>
          <tbody>
            {% for name, st in items %}
              <tr title="{{st.title}}">
                <td>
                  <span class="dot {{st.opmon_class}}"></span>{{name}}
                </td>
                <td class="right">{{st.falha}}</td>
                <td class="right">{{st.degrad}}</td>
                <td class="right">{{st.updated_human}}</td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>

    </div>

  </div>
</body>
</html>
"""
# =================================================================== #

def today_key() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def ensure_daily_reset(st: ApiState):
    tk = today_key()
    if st.day_key != tk:
        st.day_key = tk
        st.daily_falha = 0
        st.daily_degrad = 0

def run_script(path: str) -> Tuple[Optional[int], Optional[str]]:
    try:
        p = subprocess.run([path], capture_output=True, text=True, timeout=TIMEOUT_SEC)
        out = (p.stdout or "").strip()
        if p.returncode != 0:
            return None, f"rc={p.returncode} stderr={((p.stderr or '').strip()[:200])}"
        if out == "666":
            return None, "script retornou 666"
        try:
            return int(out), None
        except ValueError:
            return None, f"saida invalida: {out[:200]}"
    except Exception as e:
        return None, str(e)

def compute_color(falha: Optional[int], degrad: Optional[int], err: Optional[str]) -> Tuple[str, str, str]:
    if err is not None or falha is None or degrad is None:
        return "gray", "indefinido", "Erro/indisponível"

    has_falha = falha > 0
    has_degrad = degrad > 0

    if has_falha and has_degrad:
        return "purple", "falha+degrad", "Falha e degradação detectadas"
    if has_falha:
        return "red", "falha", "Falha detectada"
    if has_degrad:
        return "yellow", "degrad", "Degradação detectada"
    return "green", "ok", "OK"

def status_rank(color: str) -> int:
    order = {"purple": 0, "red": 1, "yellow": 2, "gray": 3, "green": 4}
    return order.get(color, 9)

# ============================ HISTORY (SQLite) ============================ #

def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts INTEGER NOT NULL,
        api TEXT NOT NULL,
        falha INTEGER,
        degrad INTEGER,
        status TEXT NOT NULL
    )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_events_ts ON events(ts)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_events_api ON events(api)")
    con.commit()
    con.close()

def log_event(api: str, falha: Optional[int], degrad: Optional[int], status: str):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO events (ts, api, falha, degrad, status) VALUES (?,?,?,?,?)",
        (int(time.time()), api,
         falha if falha is not None else None,
         degrad if degrad is not None else None,
         status)
    )
    con.commit()
    con.close()

# ========================================================================== #

def updater_loop():
    while True:
        now = time.time()
        for name, cfg in APIS.items():
            falha, err1 = run_script(cfg["falha"])
            degrad, err2 = run_script(cfg["degrad"])
            err = err1 or err2

            with LOCK:
                st = STATE[name]
                ensure_daily_reset(st)

                st.falha = falha if falha is not None else None
                st.degrad = degrad if degrad is not None else None
                st.updated_at = now
                st.error = err

                # contadores do dia
                if err is None and st.falha is not None and st.falha > 0:
                    st.daily_falha += st.falha
                if err is None and st.degrad is not None and st.degrad > 0:
                    st.daily_degrad += st.degrad

                # histórico (só quando há problema real)
                if err is None and (
                    (st.falha is not None and st.falha > 0) or
                    (st.degrad is not None and st.degrad > 0)
                ):
                    _, label, _ = compute_color(st.falha, st.degrad, None)
                    log_event(name, st.falha, st.degrad, label)

        time.sleep(INTERVAL_SEC)

def build_rows(refresh_sec: int):
    rows = []
    with LOCK:
        # regra PSC: se PSC falhou, todo mundo "fica falha" (override visual)
        psc = STATE.get("PSC")
        psc_global_down = bool(psc and psc.error is None and psc.falha is not None and psc.falha > 0)

        for name, st in STATE.items():
            ensure_daily_reset(st)

            falha_v = st.falha
            degrad_v = st.degrad
            err_v = st.error

            # override visual (não altera contadores/histórico)
            if psc_global_down and name != "PSC":
                falha_v = 1 if (falha_v is None or falha_v == 0) else falha_v
                degrad_v = 0 if degrad_v is None else degrad_v
                err_v = None

            color, label, title = compute_color(falha_v, degrad_v, err_v)

            # classe visual
            if color == "green":
                opmon_class = "ok"
            elif color == "yellow":
                opmon_class = "alert"
            elif color == "red":
                opmon_class = "crit"
            elif color == "purple":
                opmon_class = "both"
            else:
                opmon_class = "unk"

            updated_human = "nunca" if st.updated_at == 0 else time.strftime("%H:%M", time.localtime(st.updated_at))

            rows.append((name, {
                "falha": falha_v if falha_v is not None else "-",
                "degrad": degrad_v if degrad_v is not None else "-",
                "daily_falha": st.daily_falha,
                "daily_degrad": st.daily_degrad,
                "color": color,
                "label": label,
                "title": title,
                "updated_human": updated_human,
                "error": err_v,
                "opmon_class": opmon_class,
            }))

    def sort_key(item):
        name, st = item
        falha = st["falha"] if isinstance(st["falha"], int) else -1
        degrad = st["degrad"] if isinstance(st["degrad"], int) else -1
        return (
            status_rank(st["color"]),
            -(falha if falha >= 0 else 0),
            -(degrad if degrad >= 0 else 0),
            -int(st["daily_falha"]),
            -int(st["daily_degrad"]),
            name.lower(),
        )

    rows.sort(key=sort_key)

    # ===================== summary =====================
    total = len(rows)

    green = sum(1 for _, st in rows if st["color"] == "green")
    yellow = sum(1 for _, st in rows if st["color"] == "yellow")
    red = sum(1 for _, st in rows if st["color"] == "red")
    purple = sum(1 for _, st in rows if st["color"] == "purple")
    gray = sum(1 for _, st in rows if st["color"] == "gray")

    incidents = yellow + red + purple
    ok_pct = int(round((green / total) * 100)) if total > 0 else 0

    def pct(n: int) -> int:
        if total <= 0:
            return 0
        return int(round((n / total) * 100))

    summary = {
        "updated_at": time.strftime("%H:%M:%S | %d/%m/%Y", time.localtime(time.time())),
        "total": total,
        "ok": green,
        "unknown": gray,
        "yellow": yellow,
        "red": red,
        "purple": purple,
        "red_plus_purple": red + purple,
        "incidents": incidents,
        "ok_pct": ok_pct,

        "bar_green": pct(green),
        "bar_yellow": pct(yellow),
        "bar_red": pct(red),
        "bar_purple": pct(purple),
        "bar_gray": pct(gray),
        "bar_red_plus_purple": pct(red + purple),
    }
    # ===================================================

    return render_template_string(HTML, items=rows, refresh_sec=refresh_sec, summary=summary)

# ============================ E-MAIL SENDER ============================ #

def send_email_html(html: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = MAIL_SUBJECT
    msg["From"] = MAIL_FROM
    msg["To"] = ", ".join(MAIL_TO)
    msg.attach(MIMEText(html, "html", "utf-8"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as s:
        s.ehlo()
        if SMTP_USE_STARTTLS:
            s.starttls()
            s.ehlo()
        if SMTP_USER:
            s.login(SMTP_USER, SMTP_PASS)
        s.sendmail(MAIL_FROM, MAIL_TO, msg.as_string())

def render_email_html() -> str:
    with app.app_context():
        return build_rows(refresh_sec=0)

# ====================================================================== #

@app.route("/")
def index():
    return build_rows(refresh_sec=60)

@app.route("/email")
def email_view():
    return build_rows(refresh_sec=0)

@app.route("/send-email")
def send_email_route():
    html = render_email_html()
    send_email_html(html)
    return "OK"

if __name__ == "__main__":
    init_db()
    t = threading.Thread(target=updater_loop, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=9090)