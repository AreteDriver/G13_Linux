# G13 Linux Driver

A Linux kernel driver for the Logitech G13 Gameboard, providing comprehensive support for macro automation, programmable keys, RGB lighting customization, and LCD display control.

## Overview

The G13 Linux Driver is a kernel module designed to unlock the full potential of the Logitech G13 Gameboard on Linux systems. This driver enables users to harness the device's advanced features including:

- **Macro Automation**: Create and execute complex macro sequences for gaming and productivity
- **Programmable Keys**: Configure all G-keys and M-keys to perform custom actions
- **RGB Customization**: Control and customize the backlight colors to match your setup
- **LCD Display Support**: Utilize the built-in LCD screen for system information, game stats, or custom displays

The driver integrates seamlessly with the Linux kernel, providing stable and efficient communication with the G13 hardware.

## Features

- **LCD Screen Control**: Full support for the 160×43 monochrome LCD display
  - Display custom text and graphics
  - Show system information (CPU, RAM, network stats)
  - Game integration support
  
- **Macro Support**: Advanced macro recording and playback
  - Record keyboard and mouse sequences
  - Variable delay support
  - Multiple macro profiles
  
- **RGB Lighting Configuration**: Customize the backlight appearance
  - Full RGB color spectrum support
  - Adjustable brightness levels
  - Color profiles and presets
  
- **Programmable Key Mapping**: Complete control over all buttons
  - 22 programmable G-keys
  - 3 M-keys for profile switching
  - Joystick support
  
- **Linux Kernel Compatibility**: Supports Linux kernel 5.x or higher
  - Built as a loadable kernel module
  - No need to recompile the entire kernel
  - Compatible with most modern Linux distributions

## Installation Instructions

### Prerequisites

Ensure you have the necessary build tools installed:

```bash
# Debian/Ubuntu
sudo apt-get install build-essential linux-headers-$(uname -r)

# Fedora/RHEL
sudo dnf install kernel-devel kernel-headers gcc make

# Arch Linux
sudo pacman -S base-devel linux-headers
```

### Build and Install

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AreteDriver/G13LogitechOPS.git
   cd G13LogitechOPS
   ```

2. **Compile the kernel driver**:
   ```bash
   make
   ```

3. **Load the driver into the system**:
   ```bash
   sudo insmod g13.ko
   ```
   
   Or, for persistent loading across reboots:
   ```bash
   sudo make install
   sudo modprobe g13
   ```

4. **Verify the driver is loaded**:
   ```bash
   lsmod | grep g13
   dmesg | tail -n 20
   ```

### Uninstallation

To remove the driver:
```bash
sudo rmmod g13
```

To uninstall completely:
```bash
sudo make uninstall
```

## Example Commands/Screenshots

### Setting RGB Backlight Color

```bash
# Set backlight to red
echo "255 0 0" > /sys/class/g13/g13-0/rgb

# Set backlight to blue
echo "0 0 255" > /sys/class/g13/g13-0/rgb

# Set backlight to custom color (purple)
echo "128 0 128" > /sys/class/g13/g13-0/rgb
```

### LCD Display Control

```bash
# Display custom text on LCD
echo "Hello G13!" > /sys/class/g13/g13-0/lcd

# Clear the LCD
echo "" > /sys/class/g13/g13-0/lcd
```

### Screenshots and Demonstrations

*Placeholder for screenshots showcasing:*
- LCD screen with custom animations
- RGB lighting setups with different color schemes
- Key mapping configuration examples
- System monitoring on the LCD display

## Architecture Overview

The G13 Linux Driver is organized into several key modules that work together to provide comprehensive device support:

```
┌─────────────────────────────────────────────────────────────┐
│                     G13 Linux Driver                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐ │
│  │  Keymap Manager │  │   RGB Manager   │  │    LCD     │ │
│  │                 │  │                 │  │ Controller │ │
│  │ • Key Mapping   │  │ • Color Control │  │            │ │
│  │ • Macro Support │  │ • Brightness    │  │ • Display  │ │
│  │ • Profile Mgmt  │  │ • Profiles      │  │ • Graphics │ │
│  └────────┬────────┘  └────────┬────────┘  └─────┬──────┘ │
│           │                    │                  │        │
│           └────────────────────┼──────────────────┘        │
│                                │                           │
│                    ┌───────────▼──────────┐                │
│                    │   USB Communication  │                │
│                    │       Interface      │                │
│                    └───────────┬──────────┘                │
│                                │                           │
└────────────────────────────────┼───────────────────────────┘
                                 │
                        ┌────────▼─────────┐
                        │   Logitech G13   │
                        │    Gameboard     │
                        └──────────────────┘
```

### Major Components

- **Keymap Manager**: Handles all key input processing, macro execution, and profile management
- **RGB Manager**: Controls the RGB backlight system, including color selection and brightness adjustment
- **LCD Controller**: Manages the LCD display, rendering text and graphics to the screen
- **USB Communication Interface**: Low-level driver for USB communication with the G13 hardware

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Development Guidelines

- Follow the Linux kernel coding style
- Test changes thoroughly before submitting
- Document new features and API changes
- Ensure compatibility with kernel 5.x and above

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 AreteDriver

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Acknowledgments

- Logitech for creating the G13 Gameboard
- The Linux kernel development community
- All contributors to this project

## Support

For issues, questions, or feature requests, please open an issue on the [GitHub repository](https://github.com/AreteDriver/G13LogitechOPS/issues).