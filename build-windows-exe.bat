@echo off
setlocal
cd /d "%~dp0"

py -3 -m pip install --upgrade pyinstaller
py -3 -m pip install -r requirement.txt

py -3 -m PyInstaller --noconfirm --clean --onefile --noconsole --name NightHunter ^
  --add-data "api;api" ^
  --add-data "core;core" ^
  --add-data "modules;modules" ^
  --add-data "utils;utils" ^
  --add-data "frontend\dist;frontend\dist" ^
  desktop_launcher.py

echo.
echo Created: dist\NightHunter.exe
pause
