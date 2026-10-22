#!/usr/bin/env bash
# ============================================================
# NIGHT HUNTER - Instant Linux Launcher (Kali / Ubuntu / Debian)
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "         NIGHT HUNTER v1.7.0 · DEFENSIVE SECURITY OPS       "
echo "============================================================"
echo

# 1. Check Python 3
if ! command -v python3 >/dev/null 2>&1; then
  echo "[!] Error: python3 is not installed."
  echo "    Install it with: sudo apt update && sudo apt install -y python3 python3-pip python3-venv"
  exit 1
fi

PYTHON_CMD="python3"

# 2. Check if running inside existing venv or if venv exists in folder
if [ -f "$SCRIPT_DIR/.venv/bin/python" ]; then
  PYTHON_CMD="$SCRIPT_DIR/.venv/bin/python"
elif [ -f "$HOME/.local/share/NightHunter/venv/bin/python" ]; then
  PYTHON_CMD="$HOME/.local/share/NightHunter/venv/bin/python"
fi

# 3. Check for core requirements
if ! "$PYTHON_CMD" -c "import flask, requests" >/dev/null 2>&1; then
  echo "[*] First-time setup: installing dependencies..."
  if python3 -m venv "$SCRIPT_DIR/.venv" 2>/dev/null; then
    PYTHON_CMD="$SCRIPT_DIR/.venv/bin/python"
    "$PYTHON_CMD" -m pip install --upgrade pip >/dev/null 2>&1 || true
    "$PYTHON_CMD" -m pip install -r requirement.txt
  else
    pip3 install -r requirement.txt 2>/dev/null || python3 -m pip install -r requirement.txt --break-system-packages 2>/dev/null || true
  fi
fi

# 4. Launch Night Hunter
echo "[+] Starting Night Hunter engine..."
exec "$PYTHON_CMD" "$SCRIPT_DIR/main.py" "$@"
