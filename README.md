# G13 Linux

[![PyPI](https://img.shields.io/pypi/v/g13-linux)](https://pypi.org/project/g13-linux/)
[![Downloads](https://img.shields.io/pypi/dm/g13-linux)](https://pypi.org/project/g13-linux/)
[![Python](https://img.shields.io/pypi/pyversions/g13-linux)](https://pypi.org/project/g13-linux/)
[![CI](https://github.com/AreteDriver/G13_Linux/actions/workflows/ci.yml/badge.svg)](https://github.com/AreteDriver/G13_Linux/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Python userspace driver for the Logitech G13 Gaming Keyboard on Linux.

## Features

- **22 Programmable G-Keys** with macro support
- **RGB Backlight Control** with full color range
- **160x43 LCD Display** with custom text and graphics
- **Thumbstick Support** with configurable zones
- **Profile Management** for different applications
- **PyQt6 GUI** for visual configuration

## Installation

```bash
# From PyPI
pip install g13-linux

# Or with pipx (recommended for CLI tools)
pipx install g13-linux
```

### System Dependencies

```bash
# Ubuntu/Debian
sudo apt install libhidapi-hidraw0

# Fedora
sudo dnf install hidapi
```

### udev Rules (Required)

```bash
# Allow non-root access to G13
sudo cp udev/99-logitech-g13.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Usage

### CLI

```bash
g13-linux --help      # Show help
g13-linux --version   # Show version
g13-linux             # Run the input daemon
```

### GUI

```bash
g13-linux-gui         # Launch the configuration GUI
```

### Python API

```python
from g13_linux import open_g13, G13Mapper

# Open device and start mapping
device = open_g13()
mapper = G13Mapper()

# Read events
while True:
    data = read_event(device)
    if data:
        mapper.handle_raw_report(data)
```

## Hardware

| Component | Status |
|-----------|--------|
| G1-G22 Keys | ✅ Working |
| M1-M3 Mode Keys | ✅ Working |
| MR Key | ✅ Working |
| Thumbstick | ✅ Working |
| LCD Display | ✅ Working |
| RGB Backlight | ✅ Working |

**Note**: Button input requires either:
- udev rules for hidraw access, or
- `sudo` with libusb mode (`g13-linux-gui --libusb`)

Linux kernel 6.19+ will include native `hid-lg-g15` support for G13.

## Development

```bash
# Clone and setup
git clone https://github.com/AreteDriver/G13_Linux.git
cd G13_Linux
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check src/ tests/
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [PyPI Package](https://pypi.org/project/g13-linux/)
- [GitHub Issues](https://github.com/AreteDriver/G13_Linux/issues)
- [Logitech G13 Specs](https://support.logi.com/hc/en-us/articles/360024844133)
