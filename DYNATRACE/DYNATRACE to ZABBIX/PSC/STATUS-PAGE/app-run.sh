#!/bin/bash
set -euo pipefail

APP_DIR="/opt/scripts/dynatrace/status-page"
VENV="$APP_DIR/.venv"
APP="$APP_DIR/app.py"
PIDFILE="$APP_DIR/app.pid"

cd "$APP_DIR"

# Mata instância antiga (preferência: pidfile). Fallback: pkill pelo caminho do app.py.
stop_old() {
  if [[ -f "$PIDFILE" ]]; then
    oldpid="$(cat "$PIDFILE" || true)"
    if [[ -n "${oldpid:-}" ]] && kill -0 "$oldpid" 2>/dev/null; then
      echo "[INFO] Matando PID antigo via pidfile: $oldpid"
      kill "$oldpid" || true

      # espera sair
      for _ in {1..30}; do
        kill -0 "$oldpid" 2>/dev/null || break
        sleep 0.2
      done

      # se ainda estiver vivo, força
      if kill -0 "$oldpid" 2>/dev/null; then
        echo "[WARN] Ainda vivo, forçando kill -9: $oldpid"
        kill -9 "$oldpid" || true
      fi
    fi
    rm -f "$PIDFILE"
  fi

  # fallback: mata qualquer python que esteja rodando ESSE app.py
  if pgrep -f "$APP" >/dev/null 2>&1; then
    echo "[INFO] Matando processos antigos encontrados por pgrep -f '$APP'"
    pkill -f "$APP" || true
    sleep 0.5

    if pgrep -f "$APP" >/dev/null 2>&1; then
      echo "[WARN] Ainda existem processos. Forçando kill -9."
      pkill -9 -f "$APP" || true
    fi
  fi
}

stop_old

# venv + deps
if [[ ! -d "$VENV" ]]; then
  python3 -m venv "$VENV"
fi
source "$VENV/bin/activate"
pip install -r requirements.txt

# inicia em background e grava PID (pra matar certo na próxima vez)
echo "[INFO] Iniciando app: $APP"
nohup python3 "$APP" >/var/log/status-page.log 2>&1 &
echo $! > "$PIDFILE"
echo "[INFO] Novo PID: $(cat "$PIDFILE")"