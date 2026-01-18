#!/usr/bin/env python3
"""
LCD test with chunked transfers and detailed diagnostics.
"""

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

    # Detach kernel drivers
    for i in range(2):
        try:
            if dev.is_kernel_driver_active(i):
                dev.detach_kernel_driver(i)
        except Exception:
            pass

    dev.set_configuration()

    # Find the OUT endpoint on interface 1 (LCD is often on interface 1)
    cfg = dev.get_active_configuration()

    print("\nEndpoint analysis:")
    out_eps = []
    for intf in cfg:
        for ep in intf:
            if usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_OUT:
                ep_type = usb.util.endpoint_type(ep.bmAttributes)
                type_name = {1: "ISO", 2: "BULK", 3: "INT"}.get(ep_type, "?")
                print(
                    f"  Interface {intf.bInterfaceNumber}: EP 0x{ep.bEndpointAddress:02X} "
                    f"{type_name} maxPacket={ep.wMaxPacketSize}"
                )
                out_eps.append((intf.bInterfaceNumber, ep))

    # Try each OUT endpoint
    for intf_num, ep in out_eps:
        print(f"\n{'=' * 60}")
        print(f"Testing endpoint 0x{ep.bEndpointAddress:02X} on interface {intf_num}")
        print("=" * 60)

        try:
            usb.util.claim_interface(dev, intf_num)
        except Exception:
            pass

        # Build all-white pattern
        buf = bytearray(992)
        buf[0] = 0x03
        for i in range(32, 992):
            buf[i] = 0xFF

        # Method 1: Single write
        print("\n[Method 1] Single write of 992 bytes...")
        try:
            # Init LCD
            dev.ctrl_transfer(0, 9, 1, 0, None, 1000)
            written = ep.write(bytes(buf), timeout=1000)
            print(f"  Wrote {written} bytes")
        except Exception as e:
            print(f"  Error: {e}")

        input("  Press Enter to continue...")

        # Method 2: Chunked write
        print("\n[Method 2] Chunked write (64-byte chunks)...")
        try:
            dev.ctrl_transfer(0, 9, 1, 0, None, 1000)
            total = 0
            for i in range(0, 992, 64):
                chunk = bytes(buf[i : i + 64])
                written = ep.write(chunk, timeout=1000)
                total += written
            print(f"  Wrote {total} bytes in chunks")
        except Exception as e:
            print(f"  Error: {e}")

        input("  Press Enter to continue...")

        # Clear
        print("\n[Clear] All black...")
        buf = bytearray(992)
        buf[0] = 0x03
        try:
            dev.ctrl_transfer(0, 9, 1, 0, None, 1000)
            ep.write(bytes(buf), timeout=1000)
        except Exception as e:
            print(f"  Error: {e}")

        try:
            usb.util.release_interface(dev, intf_num)
        except Exception:
            pass

    # Also try direct write to endpoint address 0x02
    print(f"\n{'=' * 60}")
    print("Testing direct write to 0x02")
    print("=" * 60)

    buf = bytearray(992)
    buf[0] = 0x03
    for i in range(32, 992):
        buf[i] = 0xFF

    print("\n[Direct] Writing 992 bytes to endpoint 0x02...")
    try:
        dev.ctrl_transfer(0, 9, 1, 0, None, 1000)
        written = dev.write(0x02, bytes(buf), timeout=1000)
        print(f"  Wrote {written} bytes")
    except Exception as e:
        print(f"  Error: {e}")

    input("  Press Enter to clear and exit...")

    # Clear
    buf = bytearray(992)
    buf[0] = 0x03
    try:
        dev.ctrl_transfer(0, 9, 1, 0, None, 1000)
        dev.write(0x02, bytes(buf), timeout=1000)
    except Exception:
        pass

    print("\nDone!")


if __name__ == "__main__":
    main()
