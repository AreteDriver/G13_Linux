#!/bin/bash
echo "Searching for G13 in /dev/input/event* devices..."
echo ""

for dev in /dev/input/event*; do
    info=$(udevadm info -q property -n "$dev" 2>/dev/null)
    name=$(echo "$info" | grep "NAME=" | cut -d'"' -f2)
    id=$(echo "$info" | grep "ID_INPUT_KEYBOARD\|ID_MODEL\|ID_VENDOR_ID\|ID_MODEL_ID")

    if echo "$name" | grep -qi "g13\|Advanced Gameboard"; then
        echo "FOUND: $dev"
        echo "  Name: $name"
        echo "$id" | sed 's/^/  /'
        echo ""
    fi
done
