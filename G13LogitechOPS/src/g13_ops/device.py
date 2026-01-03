import os
import glob
import fcntl

G13_VENDOR_ID = 0x046D
G13_PRODUCT_ID = 0xC21C


def _hidiocsfeature(length):
    """HIDIOCSFEATURE ioctl for setting feature reports."""
    return 0xC0004806 | (length << 16)


def _hidiocgfeature(length):
    """HIDIOCGFEATURE ioctl for getting feature reports."""
    return 0xC0004807 | (length << 16)


class HidrawDevice:
    """Wrapper for hidraw device file to provide consistent interface."""

    def __init__(self, path):
        self.path = path
        self._fd = None
        self._file = None

    def open(self):
        self._file = open(self.path, "rb+", buffering=0)
        self._fd = self._file.fileno()
        os.set_blocking(self._fd, False)

    def read(self, size):
        try:
            data = self._file.read(size)
            return list(data) if data else None
        except BlockingIOError:
            return None

    def write(self, data):
        """Write an output report to the device."""
        return self._file.write(bytes(data))

    def send_feature_report(self, data):
        """
        Send a HID feature report to the device.

        Args:
            data: Report data (first byte should be report ID)

        Returns:
            Number of bytes written
        """
        if self._fd is None:
            raise RuntimeError("Device not open")

        buf = bytes(data)
        return fcntl.ioctl(self._fd, _hidiocsfeature(len(buf)), buf)

    def get_feature_report(self, report_id, size):
        """
        Get a HID feature report from the device.

        Args:
            report_id: Report ID to request
            size: Expected report size

        Returns:
            Report data as bytes
        """
        if self._fd is None:
            raise RuntimeError("Device not open")

        buf = bytearray(size)
        buf[0] = report_id
        fcntl.ioctl(self._fd, _hidiocgfeature(size), buf)
        return bytes(buf)

    def close(self):
        if self._file:
            self._file.close()
            self._file = None
            self._fd = None


def find_g13_hidraw():
    """Find the hidraw device path for the G13."""
    for hidraw in glob.glob("/sys/class/hidraw/hidraw*"):
        uevent_path = os.path.join(hidraw, "device", "uevent")
        try:
            with open(uevent_path, "r") as f:
                content = f.read()
                # Check for G13 HID_ID (format: 0003:0000046D:0000C21C)
                if "0000046D" in content.upper() and "0000C21C" in content.upper():
                    device_name = os.path.basename(hidraw)
                    return f"/dev/{device_name}"
        except (IOError, OSError):
            continue
    return None


def open_g13():
    """Open the G13 device and return a handle."""
    hidraw_path = find_g13_hidraw()
    if not hidraw_path:
        raise RuntimeError("Logitech G13 not found")

    device = HidrawDevice(hidraw_path)
    device.open()
    return device


def read_event(handle):
    """Read a HID report from the device."""
    data = handle.read(64)
    return data if data else None


class LibUSBDevice:
    """
    Direct libusb access for G13 input reading and LCD control.

    Required because hid-generic kernel driver consumes input reports
    and doesn't pass them to hidraw. This requires root/sudo to detach
    the kernel driver.

    G13 USB Structure:
    - Interface 0: Keyboard/keys/joystick (endpoint 1 IN)
    - Interface 1: LCD display (endpoint 2 OUT)

    Note: Linux kernel 6.19+ will have proper hid-lg-g15 support for G13.
    """

    ENDPOINT_IN = 0x81  # EP 1 IN for button/joystick data
    ENDPOINT_LCD = 0x02  # EP 2 OUT for LCD data
    REPORT_SIZE = 8  # 7 bytes data + 1 byte report ID

    def __init__(self):
        self._dev = None
        self._reattach_interfaces = []
        self._ep_in = None
        self._ep_lcd = None

    def open(self):
        """Open G13 via libusb, detaching kernel drivers from all interfaces."""
        try:
            import usb.core
            import usb.util
        except ImportError:
            raise RuntimeError("pyusb not installed. Run: pip install pyusb")

        self._dev = usb.core.find(idVendor=G13_VENDOR_ID, idProduct=G13_PRODUCT_ID)
        if self._dev is None:
            raise RuntimeError("G13 not found")

        # Detach kernel driver from all interfaces (G13 has 2)
        for intf_num in range(2):
            try:
                if self._dev.is_kernel_driver_active(intf_num):
                    self._dev.detach_kernel_driver(intf_num)
                    self._reattach_interfaces.append(intf_num)
            except Exception:
                pass

        # Set configuration
        try:
            self._dev.set_configuration()
        except Exception:
            pass

        # Claim both interfaces
        import usb.util

        for intf_num in range(2):
            try:
                usb.util.claim_interface(self._dev, intf_num)
            except Exception:
                pass

        # Find endpoints
        cfg = self._dev.get_active_configuration()

        # Interface 0: Keys/joystick input
        intf0 = cfg[(0, 0)]
        self._ep_in = usb.util.find_descriptor(
            intf0,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
            == usb.util.ENDPOINT_IN,
        )

        # Interface 1: LCD output (or interface 0 if only one interface)
        try:
            intf1 = cfg[(1, 0)]
            self._ep_lcd = usb.util.find_descriptor(
                intf1,
                custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
                == usb.util.ENDPOINT_OUT,
            )
        except (KeyError, IndexError):
            # Fall back to interface 0 OUT endpoint
            self._ep_lcd = usb.util.find_descriptor(
                intf0,
                custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
                == usb.util.ENDPOINT_OUT,
            )

    def read(self, timeout_ms=100):
        """
        Read button/joystick report.

        Returns:
            List of bytes or None on timeout
        """
        try:
            data = self._ep_in.read(64, timeout=timeout_ms)
            return list(data) if data else None
        except Exception:
            return None

    def write(self, data):
        """
        Write to LCD endpoint.

        Args:
            data: Bytes to write (992 bytes for full LCD frame)

        Returns:
            Number of bytes written
        """
        if self._ep_lcd:
            return self._ep_lcd.write(bytes(data))
        return 0

    def write_lcd(self, data):
        """
        Write LCD framebuffer data.

        Alias for write() - sends 992-byte LCD packet to endpoint 2.
        """
        return self.write(data)

    def send_feature_report(self, data):
        """Send feature report via control transfer."""
        report_id = data[0]
        return self._dev.ctrl_transfer(
            0x21,  # bmRequestType: Host-to-device, Class, Interface
            0x09,  # bRequest: SET_REPORT
            0x0300 | report_id,  # wValue: Feature report + report ID
            0,  # wIndex: Interface 0
            bytes(data),
            1000,  # timeout
        )

    def close(self):
        """Close device and reattach kernel drivers."""
        if self._dev:
            try:
                import usb.util

                # Release all claimed interfaces
                for intf_num in range(2):
                    try:
                        usb.util.release_interface(self._dev, intf_num)
                    except Exception:
                        pass

                # Reattach kernel drivers
                for intf_num in self._reattach_interfaces:
                    try:
                        self._dev.attach_kernel_driver(intf_num)
                    except Exception:
                        pass
            except Exception:
                pass
            self._dev = None
            self._ep_in = None
            self._ep_lcd = None


def open_g13_libusb():
    """
    Open G13 using libusb for input reading.

    Requires root/sudo to detach kernel driver.
    Use this when you need button/joystick input.
    """
    device = LibUSBDevice()
    device.open()
    return device
