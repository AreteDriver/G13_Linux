# G13LogitechOPS - Project Instructions

## Project Overview
Linux userspace driver for Logitech G13 gaming keypad with profile management, LCD control, and programmable macros.

**Stack**: Python, hidapi, udev
**Status**: Hardware validated, production ready

---

## Architecture

```
Hardware (G13) → USB HID → udev rules → g13-daemon → CLI/Config
```

### Key Components
- **g13_linux/** — Main package
- **configs/** — Profile YAML files
- **find_g13_device.sh** — Device detection script

### USB Details
- Vendor ID: 046d (Logitech)
- Product ID: c21c (G13)

---

## Development Workflow

```bash
# Setup
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Test (mocked, no hardware needed)
pytest

# Lint
ruff check .

# Device detection (requires G13)
sudo ./find_g13_device.sh
```

---

## Hardware Testing Status

| Feature | Code Complete | Hardware Tested | Notes |
|---------|---------------|-----------------|-------|
| Device connection | Yes | ✅ Yes | Via hidraw or libusb |
| LCD output | Yes | ✅ Yes | 5x7 font, 160x43 display |
| Backlight RGB | Yes | ✅ Yes | Full color control |
| Key detection | Yes | ✅ Yes | G1-G22, M1-M3, MR keys |
| Thumbstick | Yes | ✅ Yes | Analog position + click |
| Thumb buttons | Yes | ✅ Yes | LEFT, DOWN buttons |
| Profile switching | Yes | ✅ Yes | M1/M2/M3 mode switching |
| Joystick modes | Yes | ✅ Yes | Analog, Digital, Disabled |
| Macro recording | Yes | ✅ Yes | Recording and playback via evdev UInput |
| LCD clock | Yes | ⚠️ Untested | 12/24h, seconds, date options |

**Note**: Button/thumbstick input requires `sudo` or libusb mode to detach kernel driver.
Use `g13-linux-gui.sh` launcher for automatic privilege escalation via pkexec.

---

## Code Conventions
- Systems programming standards (careful with root privileges)
- Validate all USB input (bounds checking)
- No shell execution in macros (security)
- YAML config with JSON Schema validation
- Drop privileges after device open

---

## Portfolio Goals
This project demonstrates:
- Systems programming skills
- Hardware/software integration
- Professional documentation
- Security-conscious design
