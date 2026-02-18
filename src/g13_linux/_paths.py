"""
Path resolution for G13 Linux.

Provides consistent paths for config files, profiles, macros, and static assets
that work both in development (running from source) and when installed via pip.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Package directory (src/g13_linux/)
_PACKAGE_DIR = Path(__file__).parent

# Project root when running from source (contains configs/, gui-web/, etc.)
_SOURCE_ROOT = _PACKAGE_DIR.parent.parent

# User config directory
_USER_CONFIG_DIR = Path.home() / ".config" / "g13-linux"


def _is_source_checkout() -> bool:
    """Check if running from a source checkout (not pip-installed)."""
    return (_SOURCE_ROOT / "configs").is_dir() and (_SOURCE_ROOT / "pyproject.toml").is_file()


def get_configs_dir() -> Path:
    """Get the base configs directory.

    In development: <project_root>/configs/
    Installed: ~/.config/g13-linux/
    """
    if _is_source_checkout():
        return _SOURCE_ROOT / "configs"
    config_dir = _USER_CONFIG_DIR
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_profiles_dir() -> Path:
    """Get the profiles directory.

    In development: <project_root>/configs/profiles/
    Installed: ~/.config/g13-linux/profiles/
    """
    profiles_dir = get_configs_dir() / "profiles"
    profiles_dir.mkdir(parents=True, exist_ok=True)
    return profiles_dir


def get_macros_dir() -> Path:
    """Get the macros directory.

    In development: <project_root>/configs/macros/
    Installed: ~/.config/g13-linux/macros/
    """
    macros_dir = get_configs_dir() / "macros"
    macros_dir.mkdir(parents=True, exist_ok=True)
    return macros_dir


def get_app_profiles_path() -> Path:
    """Get the app profiles config file path.

    In development: <project_root>/configs/app_profiles.json
    Installed: ~/.config/g13-linux/app_profiles.json
    """
    return get_configs_dir() / "app_profiles.json"


def get_static_dir() -> Path:
    """Get the web GUI static files directory.

    In development: <project_root>/gui-web/dist/
    Installed: Not typically available (returns non-existent path).
    """
    if _is_source_checkout():
        return _SOURCE_ROOT / "gui-web" / "dist"
    return _PACKAGE_DIR / "static"
