# Contributing to G13LogitechOPS

Thank you for your interest in contributing to G13LogitechOPS! This project needs help from the community to bring full G13 support to Linux.

## 🎯 **How You Can Help**

### 1. Button Mapping (HIGH PRIORITY!)

The G13 has 25 programmable buttons that need to be mapped. We need help decoding the USB HID reports.

**What You Need:**
- A Logitech G13 keyboard
- Linux system
- Basic Python knowledge
- Patience for testing!

**How to Contribute:**

1. **Run the driver**:
   ```bash
   python -m g13_ops.cli
   ```

2. **Press each button and record the output**:
   - Press G1, note the RAW output
   - Press G2, note the RAW output
   - ... continue for all 25 buttons
   - Include M1, M2, M3 mode keys
   - Include joystick movements

3. **Document your findings**:
   Create a file `button_mappings.txt`:
   ```
   G1: RAW: [0, 1, 0, 0, ...]
   G2: RAW: [0, 2, 0, 0, ...]
   ...
   ```

4. **Submit a Pull Request** with your findings!

### 2. LCD Display Support

The G13 has a 160x43 pixel LCD display. We need to:
- Figure out how to send data to the LCD
- Create a text display function
- Add graphics support
- Make it useful (show profiles, stats, etc.)

### 3. Backlight Control

The G13 has RGB backlighting. We need to:
- Decode color control commands
- Create an API for setting colors
- Add profile-based color schemes

### 4. Testing

Test on different Linux distributions and report issues:
- Ubuntu/Debian
- Fedora/RHEL
- Arch Linux
- Others!

---

## 📋 **Getting Started**

### Development Setup

1. **Fork the repository**:
   - Go to https://github.com/AreteDriver/G13LogitechOPS
   - Click "Fork"

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/G13LogitechOPS.git
   cd G13LogitechOPS
   ```

3. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **Install in development mode**:
   ```bash
   pip install -e .[dev]
   ```

5. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## 💻 **Code Style**

### Python Style Guidelines

- Follow PEP 8
- Use type hints where possible
- Maximum line length: 100 characters
- Use meaningful variable names
- Document functions with docstrings

**Example**:
```python
def send_key(self, keycode: int) -> None:
    """Send a single key press and release.
    
    Args:
        keycode: Linux evdev key code to send
    """
    self.ui.write(e.EV_KEY, keycode, 1)
    self.ui.write(e.EV_KEY, keycode, 0)
    self.ui.syn()
```

### Code Formatting

We use `black` for code formatting:

```bash
# Format your code
black src/

# Check formatting
black --check src/
```

### Linting

We use `flake8` for linting:

```bash
# Check code quality
flake8 src/
```

---

## 🧪 **Testing**

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=g13_ops

# Run specific test
pytest tests/test_device.py
```

### Writing Tests

- Add tests for new features
- Test edge cases
- Mock hardware interactions

**Example**:
```python
def test_button_mapping():
    mapper = G13Mapper()
    # Test that G1 maps to KEY_1
    assert mapper.BUTTON_TO_KEY[1] == e.KEY_1
```

---

## 📝 **Commit Guidelines**

### Commit Message Format

```
type(scope): brief description

Detailed explanation if needed.

Fixes #123
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(mapper): add G1-G5 button mappings

Implemented button mappings for the first 5 G-keys based
on USB HID report analysis.

Fixes #12
```

```
docs(readme): update installation instructions

Added udev rules setup for non-root access.
```

---

## 🔄 **Pull Request Process**

1. **Update your fork**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests**:
   ```bash
   pytest
   black --check src/
   flake8 src/
   ```

3. **Push your changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create Pull Request**:
   - Go to GitHub
   - Click "New Pull Request"
   - Fill out the template
   - Link related issues

5. **Code Review**:
   - Respond to feedback
   - Make requested changes
   - Keep the conversation professional and friendly

---

## 🐛 **Reporting Bugs**

### Before Reporting

1. Check existing issues
2. Test on latest version
3. Gather debug information

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what's wrong.

**To Reproduce**
Steps to reproduce:
1. Run '...'
2. Press button '...'
3. See error

**Expected behavior**
What should happen.

**Environment:**
- OS: [Ubuntu 22.04]
- Python version: [3.10]
- G13 firmware version: [if known]

**Debug output**
```
[Paste debug output here]
```

**Additional context**
Any other relevant information.
```

---

## 💡 **Feature Requests**

We welcome feature suggestions! Please:

1. Check if it's already requested
2. Explain the use case
3. Describe the desired behavior
4. Consider implementation complexity

---

## 📖 **Documentation**

### Improving Documentation

Documentation improvements are always welcome:
- Fix typos
- Clarify confusing sections
- Add examples
- Translate to other languages

### Documentation Structure

- `README.md` - Main project documentation
- `CONTRIBUTING.md` - This file
- `docs/` - Detailed guides (planned)

---

## 🌟 **Recognition**

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project credits

---

## ❓ **Questions?**

- **General questions**: [GitHub Discussions](https://github.com/AreteDriver/G13LogitechOPS/discussions)
- **Bug reports**: [GitHub Issues](https://github.com/AreteDriver/G13LogitechOPS/issues)
- **Security issues**: Email maintainer (do not open public issue)

---

## 📜 **Code of Conduct**

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior

- Be respectful and constructive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the project

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or inflammatory comments
- Personal attacks
- Publishing others' private information

---

**Thank you for contributing to G13LogitechOPS!**

Together, we can keep the G13 alive on Linux! 🎮
