# Changelog

All notable changes to g13-linux will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.5.1] - 2026-01-06

### Fixed
- Skip pynput tests in headless CI environments (GitHub Actions)

## [1.5.0] - 2026-01-05

### Added
- **Per-Application Profiles** - automatically switch G13 profiles based on active window
  - Window monitor using xdotool (X11 only)
  - App profile rules with regex pattern matching
  - Match against window name, WM_CLASS, or both
  - Default profile fallback when no rules match
- **App Profiles Tab** in GUI for managing auto-switch rules
  - Add/Edit/Delete rules with visual editor
  - Test button shows current window info
  - Enable/disable toggle for auto-switching

### Changed
- 1110 tests with 99% coverage

## [1.4.0] - 2026-01-04

### Added
- Joystick settings tab in GUI
- Analog/Digital/Disabled joystick modes
- Deadzone and sensitivity controls
- Directional key mapping for digital mode

## [1.3.0] - 2026-01-03

### Added
- Additional test coverage improvements
- Window monitoring infrastructure

## [1.2.2] - 2026-01-03

### Added
- Desktop entry for GUI (appears in application menu)
- SVG icon with G13 keypad design
- `install-desktop.sh` for easy desktop integration

### Fixed
- GitHub Actions trusted publishing now working (no secrets needed)

## [1.2.1] - 2026-01-03

### Fixed
- Version sync after CLI subcommands release

## [1.2.0] - 2026-01-03

### Added
- CLI subcommands for hardware control:
  - `g13-linux lcd "text"` - Display text on LCD
  - `g13-linux lcd --clear` - Clear LCD display
  - `g13-linux color <color>` - Set backlight (presets, hex, RGB)
  - `g13-linux profile list|show|load|create|delete` - Profile management
- Color presets: red, green, blue, white, yellow, cyan, magenta, orange, purple, off

## [1.1.6] - 2026-01-03

### Changed
- Complete README rewrite for Python package
- Added PyPI badges (version, downloads, Python versions)

## [1.1.5] - 2026-01-03

### Added
- CLI `--help` and `--version` support

### Fixed
- Version number sync after PyPI releases

## [1.1.4] - 2026-01-03

### Added
- Packaging assets for PyPI release
- Updated release workflow

## [1.1.3] - 2026-01-03

### Fixed
- Release workflow directory structure

## [1.1.0] - 2026-01-03

### Changed
- Renamed package from `g13-ops` to `g13-linux`
- Modern `pyproject.toml` packaging
- Entry points: `g13-linux`, `g13-linux-gui`

## [1.0.0] - 2025-12-30

### Added
- **PyQt6 GUI Application** - Full graphical interface for G13 configuration
  - Visual button mapper with clickable button layout
  - Real-time button press visualization
  - Macro recording and playback
  - Profile management
  - Live event monitor
  - Hardware controls (LCD, RGB backlight)
- **Macro System** - Record and playback button sequences
  - Multiple playback modes (recorded timing, fixed delay, fast)
  - Keyboard and G13 button capture
  - JSON persistence
- **LCD Display** - 160x43 pixel monochrome display
  - 5x7 bitmap font
  - Text rendering with word wrap
  - Custom graphics support
- **RGB Backlight** - Full color control via USB feature reports
- **Button Detection** - All 22 G-keys, M1-M3, MR, thumbstick
- **Profile System** - JSON-based profiles with mappings, colors, LCD text

### Notes
- Button input requires udev rules or sudo with libusb mode
- Linux kernel 6.19+ will include native `hid-lg-g15` support

---

For detailed changes, see the [commit history](https://github.com/AreteDriver/G13_Linux/commits/main).

[Unreleased]: https://github.com/AreteDriver/G13_Linux/compare/v1.2.2...HEAD
[1.2.2]: https://github.com/AreteDriver/G13_Linux/releases/tag/v1.2.2
[1.2.1]: https://github.com/AreteDriver/G13_Linux/releases/tag/v1.2.1
[1.2.0]: https://github.com/AreteDriver/G13_Linux/releases/tag/v1.2.0
[1.1.6]: https://github.com/AreteDriver/G13_Linux/releases/tag/v1.1.6
[1.1.5]: https://github.com/AreteDriver/G13_Linux/releases/tag/v1.1.5
[1.1.4]: https://github.com/AreteDriver/G13_Linux/releases/tag/v1.1.4
[1.1.3]: https://github.com/AreteDriver/G13_Linux/releases/tag/v1.1.3
[1.1.0]: https://github.com/AreteDriver/G13_Linux/releases/tag/v1.1.0
[1.0.0]: https://github.com/AreteDriver/G13_Linux/releases/tag/v1.0.0
