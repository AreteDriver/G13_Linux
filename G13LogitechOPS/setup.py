"""Setup configuration for G13LogitechOPS"""
from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="g13-ops",
    version="1.0.0",
    author="AreteDriver",
    author_email="",
    description="Python userspace driver for the Logitech G13 Gaming Keyboard on Linux",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AreteDriver/G13LogitechOPS",
    project_urls={
        "Bug Tracker": "https://github.com/AreteDriver/G13LogitechOPS/issues",
        "Documentation": "https://github.com/AreteDriver/G13LogitechOPS#readme",
        "Source Code": "https://github.com/AreteDriver/G13LogitechOPS",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    install_requires=[
        "hidapi>=0.10.0",
        "evdev>=1.4.0",
        "PyQt6>=6.4.0",
        "pynput>=1.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "g13-ops=g13_ops.cli:main",
            "g13-ops-gui=g13_ops.gui.main:main",
        ],
    },
    keywords="logitech g13 gaming keyboard driver linux hid",
    license="MIT",
    include_package_data=True,
)
