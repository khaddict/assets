#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$ROOT_DIR/streamlit_app"
VENV_PY="$APP_DIR/venv/bin/python"

if [[ ! -x "$VENV_PY" ]]; then
  echo "Missing virtualenv Python at $VENV_PY"
  echo "Create/install dependencies first inside streamlit_app/venv"
  exit 1
fi

cleanup() {
  if [[ -n "${API_PID:-}" ]]; then kill "$API_PID" 2>/dev/null || true; fi
  if [[ -n "${UI_PID:-}" ]]; then kill "$UI_PID" 2>/dev/null || true; fi
}
trap cleanup EXIT INT TERM

cd "$APP_DIR"

"$VENV_PY" -m uvicorn pricing_api:app --host 0.0.0.0 --port 8001 &
API_PID=$!

"$VENV_PY" -m streamlit run app.py --server.headless true --server.address 0.0.0.0 --server.port 8501 &
UI_PID=$!

echo "API: http://127.0.0.1:8001/health"
echo "App: http://127.0.0.1:8501"

wait -n "$API_PID" "$UI_PID"
