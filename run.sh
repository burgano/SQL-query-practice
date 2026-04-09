#!/bin/bash
set -e
cd "$(dirname "$0")"

# On Ubuntu/Debian, python3-venv and ensurepip must be installed separately
if ! python3 -c "import ensurepip" 2>/dev/null; then
    echo "python3-venv not found. Installing..."
    PYTHON_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    sudo apt-get update -q 2>/dev/null || true
    sudo apt-get install -y "python${PYTHON_VER}-venv" python3-pip
fi

# Determine venv location - use home dir if current fs doesn't support symlinks (NTFS/exFAT)
VENV_DIR="venv"
if [ ! -f "venv/bin/activate" ]; then
    echo "Creating virtual environment..."
    rm -rf venv
    python3 -m venv venv 2>/dev/null
    if [ ! -f "venv/bin/activate" ]; then
        # Symlink failed (NTFS/exFAT mount) - create venv in home directory instead
        VENV_DIR="$HOME/.local/share/sql-query-practice-venv"
        echo "Note: filesystem does not support symlinks, using $VENV_DIR"
        rm -rf "$VENV_DIR"
        python3 -m venv "$VENV_DIR"
    fi
else
    # Check if existing venv is in home dir
    if [ -f "$HOME/.local/share/sql-query-practice-venv/bin/activate" ]; then
        VENV_DIR="$HOME/.local/share/sql-query-practice-venv"
    fi
fi

source "$VENV_DIR/bin/activate"

echo "Installing dependencies..."
pip install -r requirements.txt -q

# Find a free port starting from 5000
find_free_port() {
    local port=${1:-5000}
    while lsof -i TCP:"$port" &>/dev/null 2>&1; do
        port=$((port + 1))
    done
    echo "$port"
}

PORT=${PORT:-$(find_free_port 5000)}

echo ""
echo "Starting SQL Query Practice at http://localhost:$PORT"
echo ""

# Open browser after a short delay
OS="$(uname -s)"
if [ "$OS" = "Darwin" ]; then
    (sleep 1.5 && open "http://localhost:$PORT") &
elif [ "$OS" = "Linux" ]; then
    (sleep 1.5 && xdg-open "http://localhost:$PORT" 2>/dev/null || true) &
fi

PORT=$PORT python3 app.py
