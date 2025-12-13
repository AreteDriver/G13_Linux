# GitHub Actions CI/CD Workflows Documentation

This repository includes two GitHub Actions workflows for automated testing and deployment of the G13 Logitech kernel driver.

## Workflows Overview

### 1. Testing Pipeline (`test.yml`)

**Purpose:** Automatically builds and tests the kernel driver on every push and pull request to the main branch.

**Triggers:**
- Push to `main` branch
- Pull requests targeting `main` branch

**What it does:**
1. Checks out the repository code
2. Installs kernel driver build dependencies:
   - `build-essential` - Core compilation tools
   - `linux-headers` - Kernel headers for the running kernel
   - `kmod` - Kernel module utilities
   - `libusb-1.0-0-dev` - USB library development files
   - `pkg-config` - Package configuration tool
3. Builds the kernel driver using `make` (if Makefile exists)
4. Verifies the build by checking for `.ko` (kernel object) files
5. Runs tests if a `test` target exists in the Makefile

**Graceful Handling:**
- If no Makefile exists, the workflow skips build steps without failing
- If no test target exists, tests are skipped
- This allows the workflow to be in place before the actual driver code is committed

### 2. Deployment Pipeline (`release.yml`)

**Purpose:** Packages and publishes the kernel driver to GitHub Releases when a new version tag is created.

**Triggers:**
- Push of tags matching pattern `v*` (e.g., `v1.0.0`, `v2.1.3`)

**What it does:**
1. Checks out the repository code
2. Installs build dependencies (same as testing pipeline, plus packaging tools):
   - `debhelper` - Debian package building tools
   - `dkms` - Dynamic Kernel Module Support
3. Builds the kernel driver
4. Extracts version from the git tag
5. Creates a `.tar.gz` archive containing:
   - Compiled kernel modules (`.ko` files)
   - README.md and LICENSE files
   - Makefile for installation
   - Any installation scripts (e.g., `install.sh`)
6. Builds a `.deb` package with:
   - Proper Debian package structure
   - Automatic `depmod` execution via postinst/postrm scripts
   - Installation to `/lib/modules/$(uname -r)/extra/`
   - Documentation in `/usr/share/doc/g13-driver/`
7. Creates a GitHub Release with both artifacts and installation instructions

## Usage

### For Testing

The testing workflow runs automatically on every push and pull request. No action required from developers.

To see test results:
1. Navigate to the "Actions" tab in the GitHub repository
2. Click on the "Testing Pipeline" workflow
3. Select the relevant workflow run to see detailed logs

### For Releasing

To create a new release:

1. Ensure your code is committed and pushed to the main branch
2. Create and push a version tag:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```
3. The deployment workflow will automatically:
   - Build the driver
   - Create packages
   - Publish to GitHub Releases

4. Check the "Releases" section of the repository to find your published artifacts

### Version Numbering

Follow semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality in a backwards compatible manner  
- **PATCH**: Backwards compatible bug fixes

Examples: `v1.0.0`, `v1.1.0`, `v1.1.1`, `v2.0.0`

## Installation Instructions for Users

Users can download and install the driver from GitHub Releases:

### Using tar.gz (All Linux distributions)

```bash
# Download from GitHub Releases
wget https://github.com/AreteDriver/G13LogitechOPS/releases/download/v1.0.0/g13-driver-1.0.0.tar.gz

# Extract
tar -xzf g13-driver-1.0.0.tar.gz
cd g13-driver-1.0.0

# Install (if Makefile has install target)
sudo make install

# Or manually load the module
sudo insmod g13.ko
```

### Using .deb (Debian/Ubuntu)

```bash
# Download from GitHub Releases
wget https://github.com/AreteDriver/G13LogitechOPS/releases/download/v1.0.0/g13-driver_1.0.0.deb

# Install
sudo dpkg -i g13-driver_1.0.0.deb

# The module will be installed and depmod will be run automatically
```

## Workflow Configuration Files

- `.github/workflows/test.yml` - Testing pipeline configuration
- `.github/workflows/release.yml` - Deployment pipeline configuration
- `.gitignore` - Excludes build artifacts from version control

## Dependencies

The workflows install these packages automatically:

**Build Dependencies:**
- build-essential
- linux-headers-$(uname -r)
- kmod
- libusb-1.0-0-dev
- pkg-config

**Packaging Dependencies (release only):**
- debhelper
- dkms

## Troubleshooting

### Build fails in testing workflow

1. Check the workflow logs in the Actions tab
2. Ensure your Makefile is correctly configured for kernel module compilation
3. Verify all source files are committed to the repository

### Release workflow fails

1. Ensure the tag follows the `v*` pattern (e.g., `v1.0.0`)
2. Check that the build succeeds and produces `.ko` files
3. Verify GitHub token permissions (should be automatic for public repos)

### Package installation fails

1. Ensure you have the correct kernel headers installed on the target system
2. Check kernel version compatibility
3. Review installation logs for specific errors

## Future Enhancements

Potential improvements for these workflows:

- Add multi-kernel version testing (test against different kernel versions)
- Add static analysis tools (sparse, checkpatch.pl)
- Create RPM packages for Red Hat-based distributions
- Add code coverage reporting
- Implement automated changelog generation
- Add cross-compilation for different architectures
