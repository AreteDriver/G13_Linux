#!/usr/bin/env python3
"""Debug script to enumerate all HID devices"""
import hid

print("Enumerating all HID devices...")
print("=" * 80)

devices = hid.enumerate()
g13_devices = []

for i, dev in enumerate(devices):
    is_g13 = dev["vendor_id"] == 0x046d and dev["product_id"] == 0xc21c

    if is_g13:
        g13_devices.append(dev)
        print(f"\n*** G13 DEVICE #{len(g13_devices)} ***")
    else:
        continue  # Only show G13 devices

    print(f"Device #{i}:")
    print(f"  Path: {dev['path']}")
    print(f"  VID:PID: {dev['vendor_id']:04x}:{dev['product_id']:04x}")
    print(f"  Manufacturer: {dev['manufacturer_string']}")
    print(f"  Product: {dev['product_string']}")
    print(f"  Interface: {dev['interface_number']}")
    print(f"  Usage Page: {dev['usage_page']:#06x}")
    print(f"  Usage: {dev['usage']:#06x}")

print("\n" + "=" * 80)
print(f"Found {len(g13_devices)} G13 device interface(s)")

if g13_devices:
    print("\nAttempting to open each G13 interface...")
    for i, dev in enumerate(g13_devices):
        print(f"\nInterface #{i+1}: {dev['path']}")
        try:
            h = hid.device()
            h.open_path(dev["path"])
            print(f"  ✓ SUCCESS - Can open this interface")
            print(f"  Manufacturer: {h.get_manufacturer_string()}")
            print(f"  Product: {h.get_product_string()}")
            h.close()
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
else:
    print("\nNo G13 devices found!")
