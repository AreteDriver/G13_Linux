# Changelog

All notable changes to G13LogitechOPS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

---

## [1.0.0] - 2025-12-30

### Added
- **PyQt6 GUI Application** - Full graphical interface for G13 configuration
  - Visual button mapper with clickable button layout
  - Real-time button press visualization
  - G13 layout background image support
- **Button Mapping Tools** - Hardware reverse engineering utilities
  - `capture_buttons.py` - Interactive button capture script
  - `debug_hid.py` - Raw HID debugging tool
  - `find_g13_device.sh` - Device detection helper
  - `test_direct_read.py` - Direct USB testing
- **Event Decoder** - Improved button detection and decoding
  - 27 button position definitions
  - Joystick position tracking
  - Raw report analysis
- **Desktop Integration** - Ubuntu application launcher support
  - `g13-ops.desktop` - Main application launcher
  - `g13-capture.desktop` - Button capture launcher
- **Documentation** - Comprehensive setup and testing guides
  - Button mapping status documentation
  - Testing checklist for hardware verification
  - Background image setup instructions

### Changed
- Improved button layout positioning for visual mapper
- Enhanced G13 button widget rendering
- Updated desktop file configurations

---

## [0.2.0] - 2024-12-24

### Added
- Initial project structure
- Basic USB HID communication with G13
- Virtual input device creation using evdev
- CLI interface for running the driver
- Button mapping framework (mappings TBD)
- Profile system structure

---

## [0.1.0] - 2024-12-24

### Added
- Initial release
- Basic G13 device detection
- Raw HID report reading
- Virtual keyboard device creation
- Command-line interface
- Development environment setup
- Documentation (README, CONTRIBUTING)
- MIT License

---

## Future Versions

### [1.1.0] - Planned
- Complete G1-G25 button mappings (hardware dependent)
- Profile loading and saving system
- Basic LCD text display

### [1.2.0] - Planned
- Full joystick support and calibration
- RGB backlight control
- Systemd service for auto-start

### [2.0.0] - Planned
- Full LCD graphics support with custom images
- Profile import/export
- Application-specific profile switching

---

For detailed changes, see the [commit history](https://github.com/AreteDriver/G13LogitechOPS/commits/main).

[Unreleased]: https://github.com/AreteDriver/G13LogitechOPS/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/AreteDriver/G13LogitechOPS/releases/tag/v1.0.0
[0.2.0]: https://github.com/AreteDriver/G13LogitechOPS/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/AreteDriver/G13LogitechOPS/releases/tag/v0.1.0
