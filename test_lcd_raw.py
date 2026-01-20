#!/usr/bin/env python3
"""
Minimal LCD test - bypasses all abstractions to test raw USB protocol.
"""

import time

import usb.core
import usb.util

G13_VENDOR_ID = 0x046D
G13_PRODUCT_ID = 0xC21C


def _setup_device():
    """Find and configure the G13 device. Returns device or None."""
    print("Finding G13...")
    dev = usb.core.find(idVendor=G13_VENDOR_ID, idProduct=G13_PRODUCT_ID)
    if dev is None:
        print("G13 not found!")
        return None

    print(f"Found: {dev}")
    for i in range(2):
        try:
            if dev.is_kernel_driver_active(i):
                dev.detach_kernel_driver(i)
                print(f"Detached kernel driver from interface {i}")
        except Exception as e:
            print(f"Could not detach interface {i}: {e}")

    try:
        dev.set_configuration()
        print("Configuration set")
    except Exception as e:
        print(f"Set config: {e}")

    for i in range(2):
        try:
            usb.util.claim_interface(dev, i)
            print(f"Claimed interface {i}")
        except Exception as e:
            print(f"Claim interface {i}: {e}")

    return dev


def _print_endpoint_info(dev):
    """Print USB endpoint information."""
    cfg = dev.get_active_configuration()
    print(f"\nConfiguration: {cfg.bConfigurationValue}")
    for intf in cfg:
        print(f"\nInterface {intf.bInterfaceNumber}, Alt {intf.bAlternateSetting}")
        for ep in intf:
            direction = "IN" if usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_IN else "OUT"
            ep_type = {1: "ISO", 2: "BULK", 3: "INT"}.get(usb.util.endpoint_type(ep.bmAttributes), "?")
            print(f"  EP 0x{ep.bEndpointAddress:02X} {direction} {ep_type} maxPacket={ep.wMaxPacketSize}")


def _write_pattern(dev, buf, name):
    """Write pattern to LCD and display result."""
    print(f"\n{name}")
    try:
        print(f"    Wrote {dev.write(0x02, buf, timeout=1000)} bytes")
    except Exception as e:
        print(f"    Error: {e}")
    time.sleep(2)


def _build_patterns():
    """Build all LCD test patterns. Returns list of (name, buffer) tuples."""
    patterns = []

    # 1. All white
    buf = bytearray(992)
    buf[0] = 0x03
    for i in range(32, 992):
        buf[i] = 0xFF
    patterns.append(("[1] All white...", buf))

    # 2. All black
    buf = bytearray(992)
    buf[0] = 0x03
    patterns.append(("[2] All black...", buf))

    # 3. Vertical stripes
    buf = bytearray(992)
    buf[0] = 0x03
    for row_block in range(6):
        for x in range(0, 160, 2):
            buf[32 + x + row_block * 160] = 0xFF
    patterns.append(("[3] Vertical stripes...", buf))

    # 4. Horizontal stripes
    buf = bytearray(992)
    buf[0] = 0x03
    for row_block in [0, 2, 4]:
        for x in range(160):
            buf[32 + x + row_block * 160] = 0xFF
    patterns.append(("[4] Horizontal stripes...", buf))

    # 5. Checkerboard
    buf = bytearray(992)
    buf[0] = 0x03
    for row_block in range(6):
        for x in range(160):
            buf[32 + x + row_block * 160] = 0xAA if (x + row_block) % 2 == 0 else 0x55
    patterns.append(("[5] Checkerboard...", buf))

    # 6. Single pixel
    buf = bytearray(992)
    buf[0] = 0x03
    buf[32] = 0x01
    patterns.append(("[6] Single pixel at (0,0)...", buf))

    # 7. Top row
    buf = bytearray(992)
    buf[0] = 0x03
    for x in range(160):
        buf[32 + x] = 0x01
    patterns.append(("[7] Top row (y=0) filled...", buf))

    # 8. Clear
    buf = bytearray(992)
    buf[0] = 0x03
    patterns.append(("[8] Clear...", buf))

    return patterns


def main():
    dev = _setup_device()
    if dev is None:
        return

    _print_endpoint_info(dev)

    print("\n" + "=" * 60)
    print("Testing LCD patterns...")
    print("=" * 60)

    for name, buf in _build_patterns():
        _write_pattern(dev, buf, name)

    print("\n" + "=" * 60)
    print("Done! Check what you saw on the LCD:")
    print("  1. All white - screen should be fully lit")
    print("  2. All black - screen should be blank")
    print("  3. Vertical stripes - alternating columns")
    print("  4. Horizontal stripes - alternating bands")
    print("  5. Checkerboard - small squares")
    print("  6. Single pixel - dot in top-left")
    print("  7. Top row - horizontal line at top")
    print("  8. Clear - blank screen")
    print("=" * 60)

    for i in range(2):
        try:
            usb.util.release_interface(dev, i)
        except Exception:
            pass


if __name__ == "__main__":
    main()
