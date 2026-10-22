#!/usr/bin/env bash
# Run on Linux to create the website download: night-hunter-linux.tar.gz
set -euo pipefail

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
OUT_DIR="$ROOT_DIR/releases"
STAGE_DIR="$OUT_DIR/night-hunter-linux"

rm -rf "$STAGE_DIR"
mkdir -p "$STAGE_DIR"

for item in api core modules utils dist main.py run.sh desktop_launcher.py requirement.txt install.sh README.md USER_GUIDE.md; do
  cp -R "$ROOT_DIR/$item" "$STAGE_DIR/"
done

find "$STAGE_DIR" -type d -name '__pycache__' -prune -exec rm -rf {} +
find "$STAGE_DIR" -type f -name '*.pyc' -delete
chmod +x "$STAGE_DIR/install.sh"

tar -C "$OUT_DIR" -czf "$OUT_DIR/night-hunter-linux.tar.gz" night-hunter-linux
echo "Created: $OUT_DIR/night-hunter-linux.tar.gz"
