#!/usr/bin/env python3
"""
Minimal LCD test - bypasses all abstractions to test raw USB protocol.
"""

import time

import usb.core
import usb.util

G13_VENDOR_ID = 0x046D
G13_PRODUCT_ID = 0xC21C


def main():
    print("Finding G13...")
    dev = usb.core.find(idVendor=G13_VENDOR_ID, idProduct=G13_PRODUCT_ID)
    if dev is None:
        print("G13 not found!")
        return

    print(f"Found: {dev}")

    # Detach kernel driver
    for i in range(2):
        try:
            if dev.is_kernel_driver_active(i):
                dev.detach_kernel_driver(i)
                print(f"Detached kernel driver from interface {i}")
        except Exception as e:
            print(f"Could not detach interface {i}: {e}")

    # Set configuration
    try:
        dev.set_configuration()
        print("Configuration set")
    except Exception as e:
        print(f"Set config: {e}")

    # Claim interfaces
    for i in range(2):
        try:
            usb.util.claim_interface(dev, i)
            print(f"Claimed interface {i}")
        except Exception as e:
            print(f"Claim interface {i}: {e}")

    # Print endpoint info
    cfg = dev.get_active_configuration()
    print(f"\nConfiguration: {cfg.bConfigurationValue}")
    for intf in cfg:
        print(f"\nInterface {intf.bInterfaceNumber}, Alt {intf.bAlternateSetting}")
        for ep in intf:
            direction = (
                "IN"
                if usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_IN
                else "OUT"
            )
            ep_type = {1: "ISO", 2: "BULK", 3: "INT"}.get(
                usb.util.endpoint_type(ep.bmAttributes), "?"
            )
            print(
                f"  EP 0x{ep.bEndpointAddress:02X} {direction} {ep_type} maxPacket={ep.wMaxPacketSize}"
            )

    # Build test patterns
    print("\n" + "=" * 60)
    print("Testing LCD patterns...")
    print("=" * 60)

    # Pattern 1: All white (all pixels on)
    print("\n[1] All white...")
    buf = bytearray(992)
    buf[0] = 0x03  # Command byte
    for i in range(32, 992):
        buf[i] = 0xFF
    try:
        written = dev.write(0x02, buf, timeout=1000)
        print(f"    Wrote {written} bytes")
    except Exception as e:
        print(f"    Error: {e}")
    time.sleep(2)

    # Pattern 2: All black (all pixels off)
    print("\n[2] All black...")
    buf = bytearray(992)
    buf[0] = 0x03
    try:
        written = dev.write(0x02, buf, timeout=1000)
        print(f"    Wrote {written} bytes")
    except Exception as e:
        print(f"    Error: {e}")
    time.sleep(2)

    # Pattern 3: Vertical stripes (every other column)
    print("\n[3] Vertical stripes...")
    buf = bytearray(992)
    buf[0] = 0x03
    # Row-block layout: byte = x + (y//8)*160
    # So for x=0,2,4..., we want all bits set
    for row_block in range(6):
        for x in range(0, 160, 2):  # Every other column
            idx = 32 + x + row_block * 160
            buf[idx] = 0xFF
    try:
        written = dev.write(0x02, buf, timeout=1000)
        print(f"    Wrote {written} bytes")
    except Exception as e:
        print(f"    Error: {e}")
    time.sleep(2)

    # Pattern 4: Horizontal stripes (every other row-block)
    print("\n[4] Horizontal stripes...")
    buf = bytearray(992)
    buf[0] = 0x03
    for row_block in [0, 2, 4]:  # Every other row-block
        for x in range(160):
            idx = 32 + x + row_block * 160
            buf[idx] = 0xFF
    try:
        written = dev.write(0x02, buf, timeout=1000)
        print(f"    Wrote {written} bytes")
    except Exception as e:
        print(f"    Error: {e}")
    time.sleep(2)

    # Pattern 5: Checkerboard
    print("\n[5] Checkerboard...")
    buf = bytearray(992)
    buf[0] = 0x03
    for row_block in range(6):
        for x in range(160):
            idx = 32 + x + row_block * 160
            # Alternate pattern based on position
            if (x + row_block) % 2 == 0:
                buf[idx] = 0xAA  # 10101010
            else:
                buf[idx] = 0x55  # 01010101
    try:
        written = dev.write(0x02, buf, timeout=1000)
        print(f"    Wrote {written} bytes")
    except Exception as e:
        print(f"    Error: {e}")
    time.sleep(2)

    # Pattern 6: Single pixel test - top-left corner
    print("\n[6] Single pixel at (0,0)...")
    buf = bytearray(992)
    buf[0] = 0x03
    buf[32] = 0x01  # x=0, y=0 -> byte 32, bit 0
    try:
        written = dev.write(0x02, buf, timeout=1000)
        print(f"    Wrote {written} bytes")
    except Exception as e:
        print(f"    Error: {e}")
    time.sleep(2)

    # Pattern 7: Top row only
    print("\n[7] Top row (y=0) filled...")
    buf = bytearray(992)
    buf[0] = 0x03
    for x in range(160):
        buf[32 + x] = 0x01  # bit 0 = row 0
    try:
        written = dev.write(0x02, buf, timeout=1000)
        print(f"    Wrote {written} bytes")
    except Exception as e:
        print(f"    Error: {e}")
    time.sleep(2)

    # Final: Clear
    print("\n[8] Clear...")
    buf = bytearray(992)
    buf[0] = 0x03
    try:
        written = dev.write(0x02, buf, timeout=1000)
        print(f"    Wrote {written} bytes")
    except Exception as e:
        print(f"    Error: {e}")

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

    # Cleanup
    for i in range(2):
        try:
            usb.util.release_interface(dev, i)
        except Exception:
            pass


if __name__ == "__main__":
    main()
