#!/usr/bin/env python3
"""
LCD test with chunked transfers and detailed diagnostics.
"""

import usb.core
import usb.util

G13_VENDOR_ID = 0x046D
G13_PRODUCT_ID = 0xC21C


def _build_white_buffer():
    """Build all-white LCD buffer."""
    buf = bytearray(992)
    buf[0] = 0x03
    for i in range(32, 992):
        buf[i] = 0xFF
    return buf


def _build_black_buffer():
    """Build all-black LCD buffer."""
    buf = bytearray(992)
    buf[0] = 0x03
    return buf


def _find_out_endpoints(cfg):
    """Find all OUT endpoints and print analysis."""
    print("\nEndpoint analysis:")
    out_eps = []
    for intf in cfg:
        for ep in intf:
            if usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_OUT:
                ep_type = usb.util.endpoint_type(ep.bmAttributes)
                type_name = {1: "ISO", 2: "BULK", 3: "INT"}.get(ep_type, "?")
                print(f"  Interface {intf.bInterfaceNumber}: EP 0x{ep.bEndpointAddress:02X} "
                      f"{type_name} maxPacket={ep.wMaxPacketSize}")
                out_eps.append((intf.bInterfaceNumber, ep))
    return out_eps


def _test_endpoint(dev, intf_num, ep, buf):
    """Test LCD write methods on a specific endpoint."""
    print(f"\n{'=' * 60}")
    print(f"Testing endpoint 0x{ep.bEndpointAddress:02X} on interface {intf_num}")
    print("=" * 60)

    try:
        usb.util.claim_interface(dev, intf_num)
    except Exception:
        pass

    # Method 1: Single write
    print("\n[Method 1] Single write of 992 bytes...")
    try:
        dev.ctrl_transfer(0, 9, 1, 0, None, 1000)
        print(f"  Wrote {ep.write(bytes(buf), timeout=1000)} bytes")
    except Exception as e:
        print(f"  Error: {e}")

    input("  Press Enter to continue...")

    # Method 2: Chunked write
    print("\n[Method 2] Chunked write (64-byte chunks)...")
    try:
        dev.ctrl_transfer(0, 9, 1, 0, None, 1000)
        total = sum(ep.write(bytes(buf[i:i + 64]), timeout=1000) for i in range(0, 992, 64))
        print(f"  Wrote {total} bytes in chunks")
    except Exception as e:
        print(f"  Error: {e}")

    input("  Press Enter to continue...")

    # Clear
    print("\n[Clear] All black...")
    try:
        dev.ctrl_transfer(0, 9, 1, 0, None, 1000)
        ep.write(bytes(_build_black_buffer()), timeout=1000)
    except Exception as e:
        print(f"  Error: {e}")

    try:
        usb.util.release_interface(dev, intf_num)
    except Exception:
        pass


def main():
    print("Finding G13...")
    dev = usb.core.find(idVendor=G13_VENDOR_ID, idProduct=G13_PRODUCT_ID)
    if dev is None:
        print("G13 not found!")
        return

    for i in range(2):
        try:
            if dev.is_kernel_driver_active(i):
                dev.detach_kernel_driver(i)
        except Exception:
            pass

    dev.set_configuration()
    out_eps = _find_out_endpoints(dev.get_active_configuration())
    buf = _build_white_buffer()

    for intf_num, ep in out_eps:
        _test_endpoint(dev, intf_num, ep, buf)

    # Direct write to 0x02
    print(f"\n{'=' * 60}")
    print("Testing direct write to 0x02")
    print("=" * 60)
    print("\n[Direct] Writing 992 bytes to endpoint 0x02...")
    try:
        dev.ctrl_transfer(0, 9, 1, 0, None, 1000)
        print(f"  Wrote {dev.write(0x02, bytes(buf), timeout=1000)} bytes")
    except Exception as e:
        print(f"  Error: {e}")

    input("  Press Enter to clear and exit...")
    try:
        dev.ctrl_transfer(0, 9, 1, 0, None, 1000)
        dev.write(0x02, bytes(_build_black_buffer()), timeout=1000)
    except Exception:
        pass

    print("\nDone!")


if __name__ == "__main__":
    main()
