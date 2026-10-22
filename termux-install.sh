#!/data/data/com.termux/files/usr/bin/bash
# Installer included in night-hunter-termux.zip
set -euo pipefail

APP_NAME="NightHunter"
APP_DIR="${PREFIX}/share/${APP_NAME}"
SOURCE_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

pkg update -y
pkg install -y python nmap

rm -rf "$APP_DIR"
mkdir -p "$APP_DIR"

for item in api core modules utils dist main.py desktop_launcher.py requirement.txt README.md USER_GUIDE.md; do
  cp -R "$SOURCE_DIR/$item" "$APP_DIR/"
done

python -m pip install --upgrade pip
python -m pip install -r "$APP_DIR/requirement.txt"

cat > "${PREFIX}/bin/${APP_NAME}" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
exec python "$APP_DIR/main.py" "\$@"
EOF
chmod +x "${PREFIX}/bin/${APP_NAME}"

echo
echo "Night Hunter installed successfully in Termux."
echo "Start it with: NightHunter"
