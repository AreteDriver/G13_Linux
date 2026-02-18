"""
G13LogitechOPS GUI Entry Point

Launches the PyQt6 graphical interface for G13 configuration.

Usage:
    g13-linux-gui              # Normal mode (hidraw, no button input)
    sudo g13-linux-gui --libusb  # With button input (requires root)
"""

import atexit
import fcntl
import logging
import os
import sys
from pathlib import Path

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMessageBox

from .resources.styles import DARK_THEME

logger = logging.getLogger(__name__)

# Lock file path - prefer XDG_RUNTIME_DIR (per-user, tmpfs-backed), fallback to ~/.cache
_runtime_dir = os.environ.get("XDG_RUNTIME_DIR")
if _runtime_dir:
    LOCK_FILE = Path(_runtime_dir) / "g13-linux-gui.lock"
else:
    _cache_dir = Path.home() / ".cache" / "g13-linux"
    _cache_dir.mkdir(parents=True, exist_ok=True)
    LOCK_FILE = _cache_dir / "g13-linux-gui.lock"
_lock_file_handle = None


def acquire_instance_lock() -> bool:
    """Try to acquire single-instance lock. Returns True if acquired."""
    global _lock_file_handle
    try:
        _lock_file_handle = open(LOCK_FILE, "w")
        fcntl.flock(_lock_file_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        _lock_file_handle.write(str(os.getpid()))
        _lock_file_handle.flush()
        return True
    except OSError:
        if _lock_file_handle:
            _lock_file_handle.close()
            _lock_file_handle = None
        return False


def release_instance_lock():
    """Release the single-instance lock."""
    global _lock_file_handle
    if _lock_file_handle:
        try:
            fcntl.flock(_lock_file_handle.fileno(), fcntl.LOCK_UN)
            _lock_file_handle.close()
        except OSError:
            pass  # Best-effort unlock, file may already be closed
        _lock_file_handle = None
    try:
        LOCK_FILE.unlink(missing_ok=True)
    except OSError:
        pass  # Best-effort delete, another process may hold the lock


def main():
    """GUI application entry point"""

    # Check for --libusb flag
    use_libusb = "--libusb" in sys.argv
    if use_libusb:
        sys.argv.remove("--libusb")

    # Check for PyQt6
    try:
        from PyQt6.QtCore import QT_VERSION_STR

        mode = "libusb" if use_libusb else "hidraw"
        logger.info(f"Starting G13LogitechOPS GUI (Qt {QT_VERSION_STR}, {mode} mode)")
    except ImportError:  # pragma: no cover
        logger.error("PyQt6 not installed. Install with: pip install PyQt6")
        return 1

    # Try to acquire single-instance lock
    if not acquire_instance_lock():
        logger.error("Another instance of G13LogitechOPS GUI is already running.")
        # Show GUI message if possible
        app = QApplication(sys.argv)
        QMessageBox.warning(
            None,
            "Already Running",
            "Another instance of G13LogitechOPS GUI is already running.\n\n"
            "Only one instance can run at a time to avoid device conflicts.",
        )
        return 1

    # Register cleanup
    atexit.register(release_instance_lock)

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("G13LogitechOPS")
    app.setOrganizationName("AreteDriver")
    from .. import __version__

    app.setApplicationVersion(__version__)

    # Set default font (try platform-specific fonts)
    font = QFont("Segoe UI", 10)
    if not font.exactMatch():
        font = QFont("Ubuntu", 10)
    if not font.exactMatch():
        font = QFont("Noto Sans", 10)
    app.setFont(font)

    # Apply dark theme stylesheet
    app.setStyleSheet(DARK_THEME)

    # Import after QApplication is created
    try:
        from .controllers.app_controller import ApplicationController
        from .views.main_window import MainWindow
    except ImportError as e:
        QMessageBox.critical(
            None,
            "Import Error",
            f"Failed to import GUI components:\n{e}\n\n"
            "The GUI is still under development. Some components may be missing.",
        )
        return 1

    # Create main window
    try:
        window = MainWindow()

        # Create controller (wires everything together)
        controller = ApplicationController(window, use_libusb=use_libusb)

        # Show window
        window.show()

        # Start device monitoring
        try:
            controller.start()
        except Exception as e:
            QMessageBox.warning(
                window,
                "Device Connection",
                f"Could not connect to G13 device:\n{e}\n\n"
                "The GUI will start anyway. Connect your G13 and restart.",
            )

        # Run event loop
        return app.exec()

    except Exception as e:
        QMessageBox.critical(None, "Startup Error", f"Failed to start GUI:\n{e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
