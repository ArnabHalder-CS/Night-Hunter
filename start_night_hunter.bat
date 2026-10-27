@echo off
setlocal
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

echo ========================================================
echo        NIGHT HUNTER - DEFENSIVE SECURITY PLATFORM
echo ========================================================
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    where py >nul 2>&1
    if %errorlevel% neq 0 (
        echo [!] Python is not found in PATH.
        echo Please install Python 3.10+ from https://www.python.org/downloads/
        echo Make sure to check "Add Python to PATH" during installation.
        pause
        exit /b 1
    )
    set "PY_CMD=py -3"
) else (
    set "PY_CMD=python"
)

echo [*] Checking dependencies...
%PY_CMD% -c "import waitress, flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Installing required Python libraries...
    %PY_CMD% -m pip install -r requirement.txt
    if %errorlevel% neq 0 (
        echo [!] Failed to install dependencies.
        pause
        exit /b 1
    )
)

echo.
echo [+] Starting your local Night Hunter dashboard...
echo [+] Local Web UI will open at: http://127.0.0.1:5000
echo.
start "Night Hunter Server" cmd /k "cd /d ""%PROJECT_DIR%"" && %PY_CMD% -m waitress --listen=127.0.0.1:5000 api.server:app"
timeout /t 3 /nobreak >nul
start "" "http://127.0.0.1:5000"
