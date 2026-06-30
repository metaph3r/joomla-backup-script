#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v uname >/dev/null 2>&1; then
    echo "This script must be run on Linux or WSL."
    exit 1
fi

OS_NAME="$(uname -s)"
case "$OS_NAME" in
    Linux)
        ;;
    *)
        echo "This script creates a Linux executable. Run it from Linux or WSL, not from Windows PowerShell."
        exit 1
        ;;
esac

PYTHON_EXE=""
for candidate in "$SCRIPT_DIR/.venv/bin/python3" "$SCRIPT_DIR/.venv/bin/python" "$(command -v python3 || true)"; do
    if [[ -n "$candidate" && -x "$candidate" ]]; then
        PYTHON_EXE="$candidate"
        break
    fi
done

OUTPUT_EXE="$SCRIPT_DIR/dist/backup-joomla-site"
BUILD_DIR="$SCRIPT_DIR/dist"

if [[ -z "$PYTHON_EXE" ]]; then
    echo "No suitable Python interpreter found."
    echo "Create it first with: python3 -m venv .venv"
    exit 1
fi

echo "Using Python executable: $PYTHON_EXE"
echo "Installing PyInstaller..."
"$PYTHON_EXE" -m pip install --upgrade pyinstaller

echo "Building Linux executable..."
"$PYTHON_EXE" -m PyInstaller --noconfirm --clean --onefile --name backup-joomla-site --distpath "$BUILD_DIR" main.py
chmod +x "$OUTPUT_EXE"

echo
echo "Build complete: $OUTPUT_EXE"
