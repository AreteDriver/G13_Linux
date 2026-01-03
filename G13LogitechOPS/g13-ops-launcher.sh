#!/bin/bash
# Logitech G13 OPS Launcher Script

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate the virtual environment if it exists
if [ -d "$SCRIPT_DIR/.venv" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
fi

# Run the G13 OPS application
cd "$SCRIPT_DIR"
python3 -m g13_ops.cli

# Deactivate virtual environment on exit
deactivate 2>/dev/null
