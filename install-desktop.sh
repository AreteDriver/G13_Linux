#!/bin/bash
# Install desktop entry and icon for G13 Linux GUI

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_FILE="$SCRIPT_DIR/packaging/g13-linux.desktop"
ICON_FILE="$SCRIPT_DIR/g13-linux.svg"

# Determine install locations
if [ "$EUID" -eq 0 ]; then
    DESKTOP_DIR="/usr/share/applications"
    ICON_DIR="/usr/share/icons/hicolor/scalable/apps"
else
    DESKTOP_DIR="$HOME/.local/share/applications"
    ICON_DIR="$HOME/.local/share/icons/hicolor/scalable/apps"
fi

# Create directories
mkdir -p "$DESKTOP_DIR" "$ICON_DIR"

# Install files
cp "$DESKTOP_FILE" "$DESKTOP_DIR/g13-linux.desktop"
cp "$ICON_FILE" "$ICON_DIR/g13-linux.svg"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
fi

# Update icon cache
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f -t "$(dirname "$ICON_DIR")" 2>/dev/null || true
fi

echo "Installed G13 Linux desktop entry"
echo "  Desktop: $DESKTOP_DIR/g13-linux.desktop"
echo "  Icon: $ICON_DIR/g13-linux.svg"
