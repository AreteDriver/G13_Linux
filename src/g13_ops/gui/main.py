"""
G13LogitechOPS GUI Entry Point

Launches the PyQt6 graphical interface for G13 configuration.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMessageBox

def main():
    """GUI application entry point"""

    # Check for PyQt6
    try:
        from PyQt6.QtCore import QT_VERSION_STR
        print(f"Starting G13LogitechOPS GUI (Qt {QT_VERSION_STR})")
    except ImportError:
        print("ERROR: PyQt6 not installed. Install with: pip install PyQt6")
        return 1

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("G13LogitechOPS")
    app.setOrganizationName("AreteDriver")
    app.setApplicationVersion("0.2.0")

    # Import after QApplication is created
    try:
        from .views.main_window import MainWindow
        from .controllers.app_controller import ApplicationController
    except ImportError as e:
        QMessageBox.critical(
            None,
            "Import Error",
            f"Failed to import GUI components:\n{e}\n\n"
            "The GUI is still under development. Some components may be missing."
        )
        return 1

    # Create main window
    try:
        window = MainWindow()

        # Create controller (wires everything together)
        controller = ApplicationController(window)

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
                "The GUI will start anyway. Connect your G13 and restart."
            )

        # Run event loop
        return app.exec()

    except Exception as e:
        QMessageBox.critical(
            None,
            "Startup Error",
            f"Failed to start GUI:\n{e}"
        )
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
