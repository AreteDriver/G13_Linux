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
- **g13_ops/** — Main package
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
| Device connection | Yes | ✅ Yes | Via hidraw |
| LCD output | Yes | ✅ Yes | 5x7 font, 160x43 display |
| Backlight RGB | Yes | ✅ Yes | Full color control |
| Key detection | Yes | ⚠️ Needs sudo | Kernel driver blocks hidraw |
| Thumbstick | Yes | ⚠️ Needs sudo | Same as key detection |
| Profile switching | Yes | Partial | Depends on key detection |

**Note**: Button/thumbstick input requires `sudo` to detach kernel driver via libusb.
Linux kernel 6.19+ will have native `hid-lg-g15` support for G13.

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
