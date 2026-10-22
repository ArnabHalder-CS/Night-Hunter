#!/usr/bin/env bash
# Installer included in night-hunter-linux.tar.gz
set -euo pipefail

APP_NAME="NightHunter"
ALT_NAME="nighthunter"

# Determine user home directory safely even if run with sudo
REAL_USER="${SUDO_USER:-$USER}"
REAL_HOME=$(getent passwd "$REAL_USER" 2>/dev/null | cut -d: -f6 || echo "$HOME")
REAL_HOME="${REAL_HOME:-$HOME}"

APP_DIR="${REAL_HOME}/.local/share/${APP_NAME}"
BIN_DIR="${REAL_HOME}/.local/bin"
SOURCE_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[!] Python 3 is required. Install it with your Linux package manager (e.g. sudo apt install python3 python3-venv), then run this installer again."
  exit 1
fi

if ! command -v nmap >/dev/null 2>&1; then
  echo "[!] Nmap is not installed. Install it for the local Nmap workspace (for example: sudo apt install nmap)."
fi

mkdir -p "$APP_DIR" "$BIN_DIR"
rm -rf "$APP_DIR/app"
mkdir -p "$APP_DIR/app"

for item in api core modules utils dist main.py run.sh desktop_launcher.py requirement.txt README.md USER_GUIDE.md; do
  if [ -e "$SOURCE_DIR/$item" ]; then
    cp -R "$SOURCE_DIR/$item" "$APP_DIR/app/"
  fi
done

# Create virtual environment
if ! python3 -m venv "$APP_DIR/venv" 2>/dev/null; then
  echo "[*] Note: python3-venv not found. Falling back to system python..."
fi

if [ -f "$APP_DIR/venv/bin/python" ]; then
  PYTHON_EXEC="$APP_DIR/venv/bin/python"
  "$PYTHON_EXEC" -m pip install --upgrade pip 2>/dev/null || true
  "$PYTHON_EXEC" -m pip install -r "$APP_DIR/app/requirement.txt" 2>/dev/null || true
else
  PYTHON_EXEC="$(command -v python3)"
  pip3 install -r "$APP_DIR/app/requirement.txt" 2>/dev/null || true
fi

# Create launcher script
cat > "$BIN_DIR/$APP_NAME" <<EOF
#!/usr/bin/env bash
exec "$PYTHON_EXEC" "$APP_DIR/app/main.py" "\$@"
EOF
chmod +x "$BIN_DIR/$APP_NAME"

# Create lowercase symlink as well
ln -sf "$BIN_DIR/$APP_NAME" "$BIN_DIR/$ALT_NAME" 2>/dev/null || true

# Create desktop entry for Linux application menu
APPS_DIR="${REAL_HOME}/.local/share/applications"
mkdir -p "$APPS_DIR"
cat > "$APPS_DIR/NightHunter.desktop" <<EOF
[Desktop Entry]
Name=Night Hunter
Comment=Defensive Security Platform & Vulnerability Scanner
Exec=$BIN_DIR/$APP_NAME
Icon=$APP_DIR/app/dist/night-hunter-logo.jpeg
Terminal=false
Type=Application
Categories=Network;Security;System;
EOF
chmod +x "$APPS_DIR/NightHunter.desktop" 2>/dev/null || true

# Try to link to /usr/local/bin (which is in EVERY system's PATH)
if [ -w "/usr/local/bin" ]; then
  ln -sf "$BIN_DIR/$APP_NAME" "/usr/local/bin/$APP_NAME" 2>/dev/null || true
  ln -sf "$BIN_DIR/$APP_NAME" "/usr/local/bin/$ALT_NAME" 2>/dev/null || true
elif command -v sudo >/dev/null 2>&1; then
  sudo ln -sf "$BIN_DIR/$APP_NAME" "/usr/local/bin/$APP_NAME" 2>/dev/null || true
  sudo ln -sf "$BIN_DIR/$APP_NAME" "/usr/local/bin/$ALT_NAME" 2>/dev/null || true
fi

# Ensure ~/.local/bin is in PATH for bash, zsh, and profile
PATH_LINE='export PATH="$HOME/.local/bin:$PATH"'

for rc in "${REAL_HOME}/.bashrc" "${REAL_HOME}/.zshrc" "${REAL_HOME}/.profile"; do
  if [ -f "$rc" ]; then
    if ! grep -q '\.local/bin' "$rc"; then
      echo "" >> "$rc"
      echo '# Added by Night Hunter installer' >> "$rc"
      echo "$PATH_LINE" >> "$rc"
    fi
  fi
done

# Fix file ownership if run with sudo
if [ -n "${SUDO_USER:-}" ]; then
  chown -R "$REAL_USER:$REAL_USER" "$APP_DIR" "$BIN_DIR/$APP_NAME" "$BIN_DIR/$ALT_NAME" 2>/dev/null || true
fi

echo
echo "============================================================"
echo "   Night Hunter installed successfully!"
echo "============================================================"
echo
echo "Start it with either:"
echo "    NightHunter          (Launches Web Dashboard & opens browser)"
echo "    NightHunter --cli    (Runs in terminal CLI mode)"
echo "or:"
echo "    nighthunter"
echo
echo "If your current terminal still says 'command not found':"
echo "1. Run:  source ~/.bashrc   (or restart terminal)"
echo "2. Or run directly:  $BIN_DIR/$APP_NAME"
echo "============================================================"
