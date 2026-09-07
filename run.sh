#!/bin/bash
set -e
cd "$(dirname "$0")"

VENV_DIR=".venv"
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
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
