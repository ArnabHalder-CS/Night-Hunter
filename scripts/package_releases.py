import os
import shutil
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASES_DIR = ROOT / "releases"
RELEASES_DIR.mkdir(parents=True, exist_ok=True)

ITEMS_TO_INCLUDE = [
    "api",
    "core",
    "modules",
    "utils",
    "dist",
    "main.py",
    "run.sh",
    "requirement.txt",
    "README.md",
    "USER_GUIDE.md",
]

def clean_pycache(directory: Path):
    for root, dirs, files in os.walk(directory):
        for d in dirs:
            if d == "__pycache__":
                shutil.rmtree(Path(root) / d, ignore_errors=True)
        for f in files:
            if f.endswith(".pyc") or f.endswith(".pyo"):
                try:
                    (Path(root) / f).unlink(missing_ok=True)
                except Exception:
                    pass

def build_linux():
    stage = RELEASES_DIR / "night-hunter-linux"
    if stage.exists():
        shutil.rmtree(stage, ignore_errors=True)
    stage.mkdir(parents=True, exist_ok=True)

    for item in ITEMS_TO_INCLUDE + ["install.sh"]:
        src = ROOT / item
        if src.is_dir():
            shutil.copytree(src, stage / item, dirs_exist_ok=True)
        elif src.is_file():
            shutil.copy2(src, stage / item)

    clean_pycache(stage)

    out_tar = RELEASES_DIR / "night-hunter-linux.tar.gz"
    with tarfile.open(out_tar, "w:gz") as tar:
        tar.add(stage, arcname="night-hunter-linux")
    print(f"[+] Created: {out_tar} ({out_tar.stat().st_size} bytes)")
    shutil.rmtree(stage, ignore_errors=True)

def build_termux():
    stage = RELEASES_DIR / "night-hunter-termux"
    if stage.exists():
        shutil.rmtree(stage, ignore_errors=True)
    stage.mkdir(parents=True, exist_ok=True)

    for item in ITEMS_TO_INCLUDE:
        src = ROOT / item
        if src.is_dir():
            shutil.copytree(src, stage / item, dirs_exist_ok=True)
        elif src.is_file():
            shutil.copy2(src, stage / item)

    termux_sh = ROOT / "termux-install.sh"
    if termux_sh.is_file():
        shutil.copy2(termux_sh, stage / "install-termux.sh")

    clean_pycache(stage)

    out_zip = RELEASES_DIR / "night-hunter-termux.zip"
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(stage):
            for file in files:
                p = Path(root) / file
                arc = p.relative_to(RELEASES_DIR)
                zipf.write(p, arc)
    print(f"[+] Created: {out_zip} ({out_zip.stat().st_size} bytes)")
    shutil.rmtree(stage, ignore_errors=True)

def build_windows():
    stage = RELEASES_DIR / "night-hunter-windows"
    if stage.exists():
        shutil.rmtree(stage, ignore_errors=True)
    stage.mkdir(parents=True, exist_ok=True)

    for item in ITEMS_TO_INCLUDE:
        src = ROOT / item
        if src.is_dir():
            shutil.copytree(src, stage / item, dirs_exist_ok=True)
        elif src.is_file():
            shutil.copy2(src, stage / item)

    for item in ["start_night_hunter.bat", "run.bat", "desktop_launcher.py"]:
        src = ROOT / item
        if src.is_file():
            shutil.copy2(src, stage / item)

    clean_pycache(stage)

    out_zip = RELEASES_DIR / "night-hunter-windows.zip"
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(stage):
            for file in files:
                p = Path(root) / file
                arc = p.relative_to(RELEASES_DIR)
                zipf.write(p, arc)
    print(f"[+] Created: {out_zip} ({out_zip.stat().st_size} bytes)")
    shutil.rmtree(stage, ignore_errors=True)

if __name__ == "__main__":
    print("[*] Packaging Night Hunter v1.7.0 releases...")
    build_linux()
    build_termux()
    build_windows()
    print("[+] Packaging complete.")
