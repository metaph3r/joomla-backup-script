@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

set "PYTHON_EXE=%SCRIPT_DIR%.venv\Scripts\python.exe"
set "OUTPUT_EXE=%SCRIPT_DIR%dist\backup-joomla-site.exe"

if not exist "%PYTHON_EXE%" (
    echo Python virtual environment not found at .venv\Scripts\python.exe
    echo Create it first with: python -m venv .venv
    exit /b 1
)

echo Installing PyInstaller...
"%PYTHON_EXE%" -m pip install --upgrade pyinstaller
if errorlevel 1 (
    echo Failed to install PyInstaller.
    exit /b 1
)

echo Building executable...
"%PYTHON_EXE%" -m PyInstaller --noconfirm --clean --onefile --name backup-joomla-site --distpath "%SCRIPT_DIR%dist" "%SCRIPT_DIR%main.py"
if errorlevel 1 (
    echo Build failed.
    exit /b 1
)

echo.
echo Build complete: %OUTPUT_EXE%
pause
