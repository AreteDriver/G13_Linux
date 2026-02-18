"""Pytest configuration and fixtures for G13_Linux tests."""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Use offscreen Qt platform for headless test environments (no X11/Wayland)
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def mock_device():
    """Mock G13 device handle."""
    device = MagicMock()
    device.write.return_value = None
    device.read.return_value = bytes([0] * 8)
    return device


@pytest.fixture
def temp_config_dir(tmp_path):
    """Temporary config directory for settings tests."""
    config_dir = tmp_path / ".config" / "g13-linux"
    config_dir.mkdir(parents=True)
    return config_dir
