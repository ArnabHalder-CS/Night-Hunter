#!/usr/bin/env bash
# Run on Linux, macOS, or Git Bash to create the website download: night-hunter-termux.zip
set -euo pipefail

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
OUT_DIR="$ROOT_DIR/releases"
STAGE_DIR="$OUT_DIR/night-hunter-termux"

rm -rf "$STAGE_DIR"
mkdir -p "$STAGE_DIR"

for item in api core modules utils main.py requirement.txt termux-install.sh README.md; do
  cp -R "$ROOT_DIR/$item" "$STAGE_DIR/"
done

find "$STAGE_DIR" -type d -name '__pycache__' -prune -exec rm -rf {} +
find "$STAGE_DIR" -type f -name '*.pyc' -delete
mv "$STAGE_DIR/termux-install.sh" "$STAGE_DIR/install-termux.sh"
chmod +x "$STAGE_DIR/install-termux.sh"

(cd "$OUT_DIR" && zip -r "night-hunter-termux.zip" night-hunter-termux -x '*/__pycache__/*' '*.pyc')
echo "Created: $OUT_DIR/night-hunter-termux.zip"
