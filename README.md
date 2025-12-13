# G13 Linux Driver

## Overview

The G13 Linux Driver is a comprehensive Linux kernel driver for the Logitech G13 Gameboard. This driver enables full functionality of the Logitech G13 advanced gaming keyboard on Linux systems, providing seamless integration with modern Linux distributions.

Key capabilities include:
- **Macro Automation**: Create and execute complex macro sequences for gaming and productivity
- **Programmable Keys**: Customize all 25 programmable G-keys plus additional controls
- **RGB Customization**: Full control over RGB backlighting with customizable colors and effects
- **LCD Display Support**: Utilize the built-in 160x43 monochrome LCD screen for game stats, system information, and custom displays

This driver brings the full power of the Logitech G13 to Linux users, unlocking features previously only available on Windows.

## Features

- **LCD Screen Control**: Full support for the 160x43 pixel monochrome LCD display
  - Display custom text and graphics
  - Show system information (CPU, RAM, network stats)
  - Game integration for displaying in-game data
  - Support for screen animations and custom widgets

- **Macro Support**: Comprehensive macro programming capabilities
  - Record and playback complex key sequences
  - Timing control for precise automation
  - Multiple macro profiles for different applications
  - On-the-fly macro switching

- **RGB Lighting Configuration**: Complete control over backlighting
  - Customizable RGB color for backlight zones
  - Multiple lighting modes (static, breathing, color cycle)
  - Per-key lighting customization
  - Synchronization with other Logitech devices

- **Programmable Keys**: Full support for all G13 inputs
  - 25 programmable G-keys (G1-G25)
  - Analog joystick support
  - Mode switch keys (M1-M3) for profile switching
  - Additional modifier keys

- **Linux Kernel Compatibility**: Designed for modern Linux systems
  - Compatible with Linux kernel 5.x or higher
  - Tested on major distributions (Ubuntu, Fedora, Arch Linux)
  - Modular design for easy maintenance and updates
  - HID device integration for proper system recognition

## Installation Instructions

Follow these step-by-step instructions to install and configure the G13 Linux Driver:

### Prerequisites

Ensure you have the following installed on your system:
- Linux kernel 5.x or higher
- Kernel headers for your current kernel version
- Build essentials (gcc, make)
- Git

Install prerequisites on Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install build-essential linux-headers-$(uname -r) git
```

Install prerequisites on Fedora:
```bash
sudo dnf install kernel-devel kernel-headers gcc make git
```

Install prerequisites on Arch Linux:
```bash
sudo pacman -S base-devel linux-headers git
```

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/AreteDriver/G13LogitechOPS.git
   cd G13LogitechOPS
   ```

2. **Compile the kernel driver**
   ```bash
   make
   ```
   This will compile the G13 kernel module from source.

3. **Load the driver into the system**
   ```bash
   sudo make install
   sudo modprobe g13
   ```

4. **Verify the driver is loaded**
   ```bash
   lsmod | grep g13
   dmesg | tail -20
   ```
   You should see the g13 module listed and relevant kernel messages indicating successful initialization.

5. **Configure automatic loading (optional)**
   To load the driver automatically at boot:
   ```bash
   echo "g13" | sudo tee -a /etc/modules-load.d/g13.conf
   ```

### Uninstallation

To remove the driver:
```bash
sudo modprobe -r g13
sudo make uninstall
```

## Example Commands/Screenshots

This section provides examples of how to use the G13 Linux Driver and showcases its capabilities.

### LCD Screen Animations

*Placeholder: Screenshot showing custom animations on the G13 LCD display*

Example command to display custom text:
```bash
# Display system information on LCD
echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}')" > /sys/class/g13/lcd0/text
```

### RGB Lighting Setup

*Placeholder: Image showing different RGB lighting configurations*

Example commands for RGB control:
```bash
# Set backlight to red
echo "255,0,0" > /sys/class/g13/rgb0/color

# Set backlight to breathing blue effect
echo "breathing" > /sys/class/g13/rgb0/mode
echo "0,0,255" > /sys/class/g13/rgb0/color

# Set backlight to color cycle mode
echo "cycle" > /sys/class/g13/rgb0/mode
```

### Macro Configuration

*Placeholder: Example of macro configuration file*

Example macro definition:
```bash
# Assign a macro to G1 key
echo "macro G1 'Hello World'" > /sys/class/g13/macro0/define
```

### Joystick Calibration

*Placeholder: Screenshot of joystick calibration utility*

```bash
# View joystick input values
cat /sys/class/g13/joystick0/position
```

## Architecture Overview

The G13 Linux Driver is built with a modular architecture to ensure maintainability and extensibility. The major components include:

```
┌─────────────────────────────────────────────────────────────┐
│                     G13 Linux Driver                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Keymap     │  │     RGB      │  │     LCD      │      │
│  │   Manager    │  │   Manager    │  │  Controller  │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│         └──────────────────┼──────────────────┘              │
│                            │                                 │
│                   ┌────────▼────────┐                        │
│                   │  USB/HID Layer  │                        │
│                   └────────┬────────┘                        │
│                            │                                 │
│                   ┌────────▼────────┐                        │
│                   │ Logitech G13    │                        │
│                   │    Hardware     │                        │
│                   └─────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### Core Modules

1. **Keymap Manager**
   - Handles input from all 25 G-keys and additional buttons
   - Manages key mapping and remapping
   - Processes mode switches (M1-M3)
   - Supports multiple key profiles

2. **RGB Manager**
   - Controls RGB backlighting
   - Implements lighting effects (static, breathing, color cycle)
   - Manages color transitions and animations
   - Provides sysfs interface for user configuration

3. **LCD Controller**
   - Manages the 160x43 monochrome LCD display
   - Handles framebuffer operations
   - Supports text and graphics rendering
   - Provides interface for custom applications

4. **Macro Engine**
   - Records and plays back key sequences
   - Manages timing and delays
   - Stores macro definitions
   - Supports complex macro programming

5. **Joystick Handler**
   - Processes analog joystick input
   - Provides calibration capabilities
   - Exports joystick data to userspace
   - Supports joystick as mouse or gamepad

6. **USB/HID Layer**
   - Interfaces with Linux HID subsystem
   - Handles USB communication with device
   - Manages device initialization and cleanup
   - Processes raw HID reports

## Contributing

Contributions are welcome! If you'd like to contribute to the G13 Linux Driver:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows the Linux kernel coding style and includes appropriate documentation.

## Troubleshooting

### Driver not loading
- Ensure kernel headers match your running kernel version
- Check `dmesg` for error messages
- Verify USB connection of G13 device

### Device not recognized
- Check USB device is detected: `lsusb | grep Logitech`
- Verify proper permissions on device nodes
- Try unplugging and replugging the device

### LCD not displaying
- Verify the LCD controller module is loaded
- Check sysfs interface: `ls /sys/class/g13/lcd0/`
- Test with simple text display command

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 AreteDriver

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Acknowledgments

- Logitech for creating the G13 Gameboard
- The Linux kernel community for HID subsystem support
- Contributors and testers who help improve this driver

## Support

For issues, questions, or feature requests, please open an issue on the [GitHub repository](https://github.com/AreteDriver/G13LogitechOPS/issues).