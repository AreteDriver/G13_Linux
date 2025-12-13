# Troubleshooting Guide

This guide helps resolve common issues with the G13LogitechOPS kernel driver, focusing on kernel-space and USB connectivity problems.

---

## 📋 Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [USB Connectivity Issues](#usb-connectivity-issues)
- [Module Loading Problems](#module-loading-problems)
- [Device Recognition Issues](#device-recognition-issues)
- [Permission Problems](#permission-problems)
- [Kernel-Space Issues](#kernel-space-issues)
- [LED and LCD Problems](#led-and-lcd-problems)
- [Performance Issues](#performance-issues)
- [Advanced Debugging](#advanced-debugging)

---

## 🔍 Quick Diagnostics

Run these commands to gather system information:

```bash
# Check kernel version
uname -r

# Verify USB device
lsusb -v -d 046d:c21c

# Check module status
lsmod | grep g13

# View recent kernel messages
dmesg | tail -50 | grep -i "g13\|usb"

# Check character device
ls -l /dev/g13-*

# Verify permissions
groups $USER
```

---

## 🔌 USB Connectivity Issues

### Device Not Detected by System

**Symptoms:**
- `lsusb` doesn't show device (046d:c21c)
- No kernel messages about G13
- Device LEDs not lighting up

**Solutions:**

1. **Verify Physical Connection**
   ```bash
   # Check all USB devices
   lsusb
   
   # Monitor USB events (run this, then plug/unplug device)
   sudo udevadm monitor --environment --udev
   ```

2. **Try Different USB Port**
   ```bash
   # USB 3.0 ports sometimes have compatibility issues
   # Try USB 2.0 port
   
   # Check USB hub issues
   lsusb -t  # Shows USB tree
   ```

3. **Check USB Power Management**
   ```bash
   # Disable USB autosuspend for G13
   echo -1 | sudo tee /sys/bus/usb/devices/*/power/autosuspend_delay_ms
   
   # Or permanently in udev rules
   sudo tee -a /etc/udev/rules.d/99-g13.rules << 'EOF'
   ACTION=="add", SUBSYSTEM=="usb", ATTRS{idVendor}=="046d", ATTRS{idProduct}=="c21c", ATTR{power/autosuspend}="-1"
   EOF
   ```

4. **Reset USB Bus**
   ```bash
   # Find USB bus and device number
   lsusb | grep 046d:c21c
   # Output: Bus 001 Device 005: ID 046d:c21c
   
   # Reset the device
   sudo usbreset 001/005  # Use your bus/device numbers
   ```

### USB Device Resets Repeatedly

**Symptoms:**
- Device disconnects and reconnects
- Kernel messages show "USB disconnect" repeatedly
- Unstable operation

**Solutions:**

1. **Check Power Supply**
   ```bash
   # Monitor USB power issues
   dmesg | grep -i "power\|current"
   
   # Check if hub is powered
   lsusb -v -d 046d:c21c | grep -i "power\|maxpower"
   ```

2. **Disable USB Autosuspend**
   ```bash
   # Add kernel parameter
   sudo nano /etc/default/grub
   # Add: usbcore.autosuspend=-1
   sudo update-grub
   sudo reboot
   ```

3. **Check for IRQ Conflicts**
   ```bash
   # View IRQ assignments
   cat /proc/interrupts | grep -i usb
   
   # Check for errors
   dmesg | grep -i "irq\|error"
   ```

### USB Transfer Errors

**Symptoms:**
- "USB transfer error" in kernel log
- Failed write operations
- Incomplete data transfer

**Solutions:**

1. **Check USB Controller**
   ```bash
   # Identify USB controller
   lspci | grep -i usb
   
   # Check controller messages
   dmesg | grep -i xhci
   ```

2. **Reduce Transfer Size**
   ```bash
   # Load module with smaller buffer
   sudo modprobe g13 buffer_size=512
   ```

3. **Update USB Firmware**
   ```bash
   # Check for firmware updates
   sudo fwupdmgr get-devices
   sudo fwupdmgr update
   ```

---

## 🔧 Module Loading Problems

### Module Fails to Load

**Symptoms:**
- `modprobe g13` returns error
- "Unknown symbol" errors
- "Invalid module format"

**Solutions:**

1. **Kernel Version Mismatch**
   ```bash
   # Check module info
   modinfo g13.ko | grep vermagic
   
   # Compare with running kernel
   uname -r
   
   # Rebuild for current kernel
   make clean
   make
   sudo make install
   ```

2. **Missing Dependencies**
   ```bash
   # Check module dependencies
   modinfo g13.ko | grep depends
   
   # Load dependencies first
   sudo modprobe usbhid
   sudo modprobe hid-generic
   sudo modprobe g13
   ```

3. **Symbol Resolution Errors**
   ```bash
   # View detailed error
   sudo dmesg | tail -20
   
   # Update module dependencies
   sudo depmod -a
   
   # Try loading again
   sudo modprobe g13
   ```

### Module Loads But Device Doesn't Work

**Symptoms:**
- Module loaded (`lsmod` shows g13)
- No `/dev/g13-*` device
- No response from hardware

**Solutions:**

1. **Check Module Parameters**
   ```bash
   # View current parameters
   systool -v -m g13
   
   # Reload with debug
   sudo modprobe -r g13
   sudo modprobe g13 debug=3
   
   # Check kernel log
   dmesg | tail -30
   ```

2. **Verify Device Binding**
   ```bash
   # Check if driver bound to device
   ls -l /sys/bus/usb/drivers/g13/
   
   # Manually bind if needed
   echo "1-1:1.0" | sudo tee /sys/bus/usb/drivers/g13/bind
   ```

---

## 🎯 Device Recognition Issues

### Driver Doesn't Claim Device

**Symptoms:**
- Generic HID driver claims device instead
- G13 driver not binding to hardware

**Solutions:**

1. **Unbind Generic Driver**
   ```bash
   # Find device in sysfs
   find /sys/bus/usb/devices -name "046d:c21c"
   
   # Unbind generic driver
   echo "1-1:1.0" | sudo tee /sys/bus/usb/drivers/usbhid/unbind
   
   # Bind G13 driver
   echo "1-1:1.0" | sudo tee /sys/bus/usb/drivers/g13/bind
   ```

2. **Blacklist Conflicting Drivers**
   ```bash
   # Create blacklist
   sudo tee /etc/modprobe.d/g13-blacklist.conf << 'EOF'
   # Prevent generic HID from claiming G13
   blacklist hid_logitech
   EOF
   
   # Update initramfs
   sudo update-initramfs -u
   ```

### Multiple Devices Not Recognized

**Symptoms:**
- Only first G13 detected
- Second device creates no `/dev/g13-1`

**Solutions:**

1. **Check Device Limit**
   ```bash
   # Module may have device limit
   # Reload with higher limit
   sudo modprobe -r g13
   sudo modprobe g13 max_devices=4
   ```

2. **Check Minor Numbers**
   ```bash
   # View allocated minors
   cat /proc/devices | grep g13
   
   # Check dynamic allocation
   ls -l /sys/class/g13/
   ```

---

## 🔒 Permission Problems

### Cannot Access `/dev/g13-*`

**Symptoms:**
- "Permission denied" when writing to device
- Works with sudo but not as regular user

**Solutions:**

1. **Add User to Correct Group**
   ```bash
   # Check device group
   ls -l /dev/g13-*
   # Output: crw-rw---- 1 root plugdev 245, 0
   
   # Add user to group
   sudo usermod -a -G plugdev $USER
   
   # Verify membership
   groups $USER
   
   # Log out and back in, or:
   newgrp plugdev
   ```

2. **Fix udev Rules**
   ```bash
   # Verify udev rule exists
   cat /etc/udev/rules.d/99-g13.rules
   
   # If missing, create it:
   sudo tee /etc/udev/rules.d/99-g13.rules << 'EOF'
   SUBSYSTEM=="usb", ATTRS{idVendor}=="046d", ATTRS{idProduct}=="c21c", MODE="0660", GROUP="plugdev"
   KERNEL=="g13-[0-9]*", MODE="0660", GROUP="plugdev"
   EOF
   
   # Reload rules
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

3. **Check SELinux/AppArmor**
   ```bash
   # Check SELinux status
   getenforce
   
   # Temporarily disable for testing
   sudo setenforce 0
   
   # For permanent fix, create policy
   # Or add to permissive:
   sudo semanage permissive -a g13_t
   ```

---

## ⚙️ Kernel-Space Issues

### Kernel Panic or Oops

**Symptoms:**
- System crashes when loading module
- Kernel oops messages
- System freeze

**Solutions:**

1. **Capture Crash Information**
   ```bash
   # Enable kernel crash dumps
   sudo apt-get install kdump-tools
   sudo systemctl enable kdump
   
   # View crash logs
   sudo crash /var/crash/...
   ```

2. **Load in Debug Mode**
   ```bash
   # Load with maximum debugging
   sudo modprobe g13 debug=5
   
   # Monitor in separate terminal
   sudo dmesg -w
   ```

3. **Check Stack Traces**
   ```bash
   # View detailed crash
   sudo journalctl -k -b -1
   
   # Look for:
   # - NULL pointer dereference
   # - Invalid memory access
   # - Spinlock issues
   ```

### Memory Leaks

**Symptoms:**
- System memory gradually decreases
- Module unload hangs
- `kmemleak` warnings

**Solutions:**

1. **Enable Kernel Memory Leak Detector**
   ```bash
   # Check if enabled
   cat /sys/kernel/debug/kmemleak
   
   # Trigger scan
   echo scan | sudo tee /sys/kernel/debug/kmemleak
   
   # View results
   cat /sys/kernel/debug/kmemleak
   ```

2. **Monitor Module Memory**
   ```bash
   # Check memory usage
   cat /proc/slabinfo | grep g13
   
   # Monitor over time
   watch -n 1 'cat /proc/slabinfo | grep g13'
   ```

### Race Conditions

**Symptoms:**
- Intermittent failures
- Works sometimes, fails others
- Deadlocks or hangs

**Solutions:**

1. **Enable Lock Debugging**
   ```bash
   # Check kernel config
   grep LOCKDEP /boot/config-$(uname -r)
   
   # View lock warnings
   dmesg | grep -i "lock\|deadlock"
   ```

2. **Use Dynamic Debug**
   ```bash
   # Enable function tracing
   echo 'module g13 +p' | sudo tee /sys/kernel/debug/dynamic_debug/control
   
   # View trace
   sudo cat /sys/kernel/debug/tracing/trace
   ```

---

## 💡 LED and LCD Problems

### LED Doesn't Change Color

**Symptoms:**
- LED stays same color
- Commands accepted but no effect

**Solutions:**

1. **Verify Command Format**
   ```bash
   # Correct format: "led R G B" (0-255 each)
   echo "led 255 0 0" | sudo tee /dev/g13-0
   
   # Check device response
   dmesg | tail -5
   ```

2. **Check USB Transfer**
   ```bash
   # Enable USB debugging
   echo Y | sudo tee /sys/module/usbcore/parameters/usbfs_snoop
   
   # Monitor USB traffic
   sudo cat /sys/kernel/debug/usb/usbmon/0u
   ```

### LCD Not Displaying

**Symptoms:**
- LCD remains blank
- No response to commands

**Solutions:**

1. **Check LCD Initialization**
   ```bash
   # Verify initialization in logs
   dmesg | grep -i "lcd\|display"
   
   # Try re-initialization
   echo "lcd_reset" | sudo tee /dev/g13-0
   ```

2. **Test with Simple Pattern**
   ```bash
   # Fill LCD with test pattern
   echo "lcd_fill 0xFF" | sudo tee /dev/g13-0
   
   # Clear LCD
   echo "lcd_clear" | sudo tee /dev/g13-0
   ```

3. **Verify Framebuffer Format**
   ```bash
   # Check framebuffer size (160x43 pixels = 860 bytes)
   # Bits are packed: 160 * 43 / 8 = 860
   dd if=/dev/zero bs=860 count=1 | sudo tee /dev/g13-0
   ```

---

## ⚡ Performance Issues

### High CPU Usage

**Symptoms:**
- Kernel threads consuming CPU
- System slowdown with G13 connected

**Solutions:**

1. **Check Interrupt Rate**
   ```bash
   # Monitor interrupts
   watch -n 1 'cat /proc/interrupts | grep g13'
   
   # Reduce polling rate if applicable
   echo "poll_interval 100" | sudo tee /dev/g13-0
   ```

2. **Profile Kernel Functions**
   ```bash
   # Use perf to identify hot spots
   sudo perf top -k
   
   # Or specific to module
   sudo perf record -g -a sleep 10
   sudo perf report
   ```

### Input Lag

**Symptoms:**
- Delayed key response
- Macro execution lag

**Solutions:**

1. **Check Input Queue**
   ```bash
   # Increase input buffer
   echo 128 | sudo tee /sys/module/g13/parameters/input_buffer_size
   ```

2. **Verify Interrupt Priority**
   ```bash
   # Check if using threaded IRQ
   ps aux | grep "irq.*g13"
   
   # Increase priority
   sudo chrt -f -p 80 $(pgrep "irq.*g13")
   ```

---

## 🔬 Advanced Debugging

### Enable Verbose Logging

```bash
# Load module with all debug options
sudo modprobe g13 debug=5

# Enable dynamic debug for specific functions
echo 'file g13.c +p' | sudo tee /sys/kernel/debug/dynamic_debug/control

# Enable function tracing
cd /sys/kernel/debug/tracing
echo function > current_tracer
echo g13_* > set_ftrace_filter
echo 1 > tracing_on
cat trace
```

### USB Protocol Analysis

```bash
# Install Wireshark for USB
sudo apt-get install wireshark tshark

# Capture USB traffic (requires usbmon module)
sudo modprobe usbmon
sudo wireshark

# Or command line:
sudo tshark -i usbmon1 -f "usb.device_address == X"
```

### Kernel Debugging with GDB

```bash
# Build module with debug symbols
make EXTRA_CFLAGS="-g -O0"

# Use QEMU/KVM for kernel debugging
# Or on live system (dangerous):
sudo gdb /usr/lib/debug/boot/vmlinux-$(uname -r)
(gdb) target remote /proc/kcore
(gdb) lx-symbols
```

### Check System Logs

```bash
# View all relevant logs
sudo journalctl -k | grep -i "g13\|usb\|hid"

# Follow live
sudo journalctl -kf

# With timestamps
sudo journalctl -k --since "10 minutes ago"

# Export for analysis
sudo journalctl -k > /tmp/kernel.log
```

---

## 📊 Diagnostic Script

Create a comprehensive diagnostic script:

```bash
#!/bin/bash
# g13_diagnostics.sh - Comprehensive G13 diagnostic tool

echo "=== G13 Diagnostic Report ==="
echo "Generated: $(date)"
echo

echo "=== System Information ==="
uname -a
echo

echo "=== Kernel Modules ==="
lsmod | grep -E "g13|hid|usb"
echo

echo "=== USB Devices ==="
lsusb | grep 046d:c21c
echo

echo "=== Character Devices ==="
ls -l /dev/g13-* 2>/dev/null || echo "No G13 devices found"
echo

echo "=== Recent Kernel Messages ==="
dmesg | grep -i g13 | tail -20
echo

echo "=== Module Information ==="
modinfo g13 2>/dev/null || echo "Module not installed"
echo

echo "=== USB Details ==="
lsusb -v -d 046d:c21c 2>/dev/null || echo "Device not connected"
echo

echo "=== Permissions ==="
echo "User: $USER"
echo "Groups: $(groups)"
echo

echo "=== udev Rules ==="
cat /etc/udev/rules.d/99-g13.rules 2>/dev/null || echo "No udev rules found"
```

---

## 🆘 Getting Help

If problems persist:

1. **Gather Information**
   ```bash
   # Run diagnostic script
   ./g13_diagnostics.sh > g13_report.txt
   ```

2. **Check Existing Issues**
   - Search [GitHub Issues](https://github.com/AreteDriver/G13LogitechOPS/issues)

3. **Report New Issue**
   - Include diagnostic output
   - Describe symptoms and steps to reproduce
   - List kernel version and distribution

4. **Community Resources**
   - [GitHub Discussions](https://github.com/AreteDriver/G13LogitechOPS/discussions)
   - Linux USB mailing lists
   - Distribution-specific forums

---

## 📚 Additional Resources

- [Linux USB FAQ](https://www.linux-usb.org/FAQ.html)
- [Kernel Documentation: USB](https://www.kernel.org/doc/html/latest/driver-api/usb/index.html)
- [Kernel Documentation: HID](https://www.kernel.org/doc/html/latest/hid/index.html)
- [Debugging kernel modules](https://www.kernel.org/doc/html/latest/dev-tools/kgdb.html)

---

For installation issues, see [INSTALLATION.md](INSTALLATION.md).
