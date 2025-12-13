# Installation Guide

This guide provides detailed instructions for building, installing, and configuring the G13LogitechOPS kernel driver.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [System Requirements](#system-requirements)
- [Dependencies](#dependencies)
- [Building from Source](#building-from-source)
- [Installing the Module](#installing-the-module)
- [Loading the Module](#loading-the-module)
- [Verification](#verification)
- [Uninstallation](#uninstallation)
- [Advanced Configuration](#advanced-configuration)

---

## Prerequisites

### System Requirements

- **Operating System**: Linux kernel 4.4 or higher
- **Architecture**: x86_64 (amd64), ARM64 (experimental)
- **USB Support**: USB 2.0 or higher
- **Hardware**: Logitech G13 Gaming Keyboard (USB ID: 046d:c21c)

### Required Permissions

You'll need:
- Root access (sudo) for module installation
- User membership in `plugdev` or `input` group for device access

---

## 🔧 Dependencies

### Build Dependencies

Install the following packages before building:

#### Debian/Ubuntu

```bash
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    linux-headers-$(uname -r) \
    linux-source \
    kmod \
    git \
    pkg-config \
    libusb-1.0-0-dev
```

#### Fedora/RHEL/CentOS

```bash
sudo dnf install -y \
    kernel-devel \
    kernel-headers \
    gcc \
    make \
    git \
    kmod \
    libusb-devel
```

#### Arch Linux

```bash
sudo pacman -S \
    linux-headers \
    base-devel \
    git \
    libusb
```

#### openSUSE

```bash
sudo zypper install -y \
    kernel-devel \
    kernel-default-devel \
    gcc \
    make \
    git \
    libusb-1_0-devel
```

### Runtime Dependencies

- **udev**: For device detection and permissions
- **kmod**: For module loading/unloading
- **libusb**: For USB communication

---

## 🏗️ Building from Source

### 1. Clone the Repository

```bash
git clone https://github.com/AreteDriver/G13LogitechOPS.git
cd G13LogitechOPS
```

### 2. Verify Kernel Headers

Ensure kernel headers match your running kernel:

```bash
# Check running kernel version
uname -r

# Verify headers are installed
ls /lib/modules/$(uname -r)/build
```

If headers are missing:

```bash
# Debian/Ubuntu
sudo apt-get install linux-headers-$(uname -r)

# Fedora/RHEL
sudo dnf install kernel-devel-$(uname -r)
```

### 3. Build the Module

```bash
# Clean any previous build artifacts
make clean

# Build the kernel module
make

# Check build output
ls -l *.ko
```

Expected output:
```
g13.ko
```

### 4. Optional: Build User-Space Tools

```bash
# Build LCD image loader
make tools

# Build all utilities
make all
```

---

## 📦 Installing the Module

### Method 1: Manual Installation (Recommended for Testing)

```bash
# Install module to system
sudo make install

# Update module dependencies
sudo depmod -a
```

### Method 2: DKMS Installation (Recommended for Automatic Updates)

DKMS (Dynamic Kernel Module Support) automatically rebuilds the module when kernel is updated.

```bash
# Install DKMS if not present
sudo apt-get install dkms  # Debian/Ubuntu
sudo dnf install dkms       # Fedora/RHEL

# Copy source to DKMS tree
sudo cp -r . /usr/src/g13-1.0

# Create DKMS configuration
sudo tee /usr/src/g13-1.0/dkms.conf << EOF
PACKAGE_NAME="g13"
PACKAGE_VERSION="1.0"
BUILT_MODULE_NAME[0]="g13"
DEST_MODULE_LOCATION[0]="/kernel/drivers/hid"
AUTOINSTALL="yes"
EOF

# Add to DKMS
sudo dkms add -m g13 -v 1.0

# Build with DKMS
sudo dkms build -m g13 -v 1.0

# Install with DKMS
sudo dkms install -m g13 -v 1.0
```

### Method 3: Package Installation (Distribution-Specific)

Create a distribution package for easier deployment:

#### Debian/Ubuntu (.deb)

```bash
# Install packaging tools
sudo apt-get install dkms debhelper

# Build package
make deb

# Install package
sudo dpkg -i g13-dkms_1.0_all.deb
```

#### Fedora/RHEL (.rpm)

```bash
# Install packaging tools
sudo dnf install rpm-build

# Build package
make rpm

# Install package
sudo rpm -i g13-kmod-1.0.rpm
```

---

## 🚀 Loading the Module

### Automatic Loading (Recommended)

Configure the module to load automatically on boot:

```bash
# Add module to load on boot
echo "g13" | sudo tee -a /etc/modules-load.d/g13.conf

# Set module parameters (optional)
sudo tee /etc/modprobe.d/g13.conf << EOF
# G13 driver options
options g13 debug=0
options g13 default_rgb=0,255,0
EOF

# Reload systemd
sudo systemctl daemon-reload
```

### Manual Loading

Load the module manually:

```bash
# Load the module
sudo modprobe g13

# Or using insmod
sudo insmod g13.ko
```

### Load with Parameters

```bash
# Load with debug enabled
sudo modprobe g13 debug=1

# Load with custom default LED color (RGB)
sudo modprobe g13 default_rgb=255,0,0
```

---

## ✅ Verification

### 1. Check Module is Loaded

```bash
# List loaded modules
lsmod | grep g13

# Expected output:
# g13                    16384  0
```

### 2. Verify Device Detection

```bash
# Check USB device
lsusb | grep "046d:c21c"

# Expected output:
# Bus 001 Device 003: ID 046d:c21c Logitech, Inc. G13 Advanced Gameboard
```

### 3. Check Kernel Messages

```bash
# View module load messages
dmesg | tail -20 | grep g13

# Expected output:
# [12345.678901] g13: Logitech G13 driver v1.0
# [12345.678902] g13: Device detected: Logitech G13
# [12345.678903] g13: Registered input device
# [12345.678904] g13: Created character device /dev/g13-0
```

### 4. Verify Character Device

```bash
# Check device file exists
ls -l /dev/g13-*

# Expected output:
# crw-rw---- 1 root plugdev 245, 0 Dec 13 10:00 /dev/g13-0
```

### 5. Test Basic Functionality

```bash
# Test LED control
echo "led 255 0 0" | sudo tee /dev/g13-0

# Test LCD
echo "lcd_text 'Test'" | sudo tee /dev/g13-0
```

---

## 🔐 Setting Up Permissions

### udev Rules

Configure udev to allow non-root access:

```bash
# Create udev rule
sudo tee /etc/udev/rules.d/99-g13.rules << 'EOF'
# Logitech G13 Gaming Keyboard
SUBSYSTEM=="usb", ATTRS{idVendor}=="046d", ATTRS{idProduct}=="c21c", MODE="0660", GROUP="plugdev"
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="046d", ATTRS{idProduct}=="c21c", MODE="0660", GROUP="plugdev"
KERNEL=="g13-[0-9]*", MODE="0660", GROUP="plugdev"
EOF

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger

# Add user to plugdev group
sudo usermod -a -G plugdev $USER

# Log out and back in for group changes to take effect
```

---

## 🗑️ Uninstallation

### Remove Module

```bash
# Unload module
sudo modprobe -r g13

# Or using rmmod
sudo rmmod g13
```

### Uninstall from System

#### Manual Installation

```bash
# Remove module file
sudo make uninstall

# Update dependencies
sudo depmod -a
```

#### DKMS Installation

```bash
# Remove from DKMS
sudo dkms remove g13/1.0 --all

# Remove source
sudo rm -rf /usr/src/g13-1.0
```

#### Package Installation

```bash
# Debian/Ubuntu
sudo apt-get remove g13-dkms

# Fedora/RHEL
sudo dnf remove g13-kmod
```

### Clean Up Configuration

```bash
# Remove autoload configuration
sudo rm /etc/modules-load.d/g13.conf
sudo rm /etc/modprobe.d/g13.conf

# Remove udev rules
sudo rm /etc/udev/rules.d/99-g13.rules
sudo udevadm control --reload-rules
```

---

## 🔧 Advanced Configuration

### Module Parameters

Available module parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `debug` | int | 0 | Debug level (0-5) |
| `default_rgb` | string | "0,255,0" | Default LED color (R,G,B) |
| `lcd_brightness` | int | 128 | LCD backlight (0-255) |
| `enable_stick` | bool | true | Enable analog stick |

Example:

```bash
sudo modprobe g13 debug=2 default_rgb=255,128,0 lcd_brightness=200
```

### Kernel Command Line

Add module parameters to kernel boot:

```bash
# Edit GRUB configuration
sudo nano /etc/default/grub

# Add to GRUB_CMDLINE_LINUX:
# g13.debug=1 g13.default_rgb=0,255,0

# Update GRUB
sudo update-grub  # Debian/Ubuntu
sudo grub2-mkconfig -o /boot/grub2/grub.cfg  # Fedora/RHEL
```

### Debugging

Enable debug output:

```bash
# Load with maximum debug
sudo modprobe g13 debug=5

# View debug messages
sudo dmesg -w | grep g13

# Or using journalctl
sudo journalctl -kf | grep g13
```

---

## 🐛 Build Troubleshooting

### Issue: "No rule to make target 'modules'"

**Solution**: Kernel headers not properly installed

```bash
sudo apt-get install --reinstall linux-headers-$(uname -r)
```

### Issue: "gcc: error: unrecognized command line option"

**Solution**: Compiler version mismatch

```bash
# Check required GCC version
cat /proc/version

# Install matching GCC
sudo apt-get install gcc-XX  # Replace XX with version
```

### Issue: "Module verification failed"

**Solution**: Disable Secure Boot or sign the module

```bash
# Option 1: Disable Secure Boot in BIOS

# Option 2: Sign the module
sudo /usr/src/linux-headers-$(uname -r)/scripts/sign-file \
    sha256 \
    /path/to/signing_key.priv \
    /path/to/signing_key.x509 \
    g13.ko
```

---

## 📚 Additional Resources

- [Kernel Module Programming Guide](https://www.kernel.org/doc/html/latest/kbuild/modules.html)
- [USB HID Documentation](https://www.kernel.org/doc/html/latest/hid/index.html)
- [DKMS Documentation](https://help.ubuntu.com/community/DKMS)

---

For troubleshooting runtime issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
