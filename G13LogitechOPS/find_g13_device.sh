#!/bin/bash
# Find which /dev/hidraw device is the G13

echo "==================================================================="
echo "G13 DEVICE FINDER"
echo "==================================================================="
echo ""
echo "Checking all /dev/hidraw devices for G13..."
echo ""

for device in /dev/hidraw*; do
    if [ -r "$device" ]; then
        echo "Testing: $device"

        # Try to read device info using udevadm
        udev_info=$(udevadm info -q all -n "$device" 2>/dev/null | grep -i "046d.*c21c")

        if [ -n "$udev_info" ]; then
            echo "  ✓ FOUND G13 at $device!"
            echo "  $udev_info"
            echo ""
            echo "Use this device: $device"
            echo "Run: sed -i 's|/dev/hidraw3|$device|g' capture_buttons.py"
            exit 0
        fi
    fi
done

echo ""
echo "G13 not found in any /dev/hidraw device"
echo "Make sure G13 is plugged in and udev rules are loaded"
