"""
G13 Daemon

Main orchestrator for G13 device management.
Coordinates input handling, LCD menu, LED effects, and key mapping.
"""

import logging
import signal
import sys
import threading
import time
from datetime import datetime

from .device import open_g13
from .gui.models.profile_manager import ProfileManager
from .hardware.backlight import G13Backlight
from .hardware.lcd import G13LCD
from .input.handler import InputHandler
from .input.navigation import NavigationController
from .led.controller import LEDController
from .mapper import G13Mapper
from .menu.manager import ScreenManager
from .menu.screen import InputEvent
from .menu.screens.idle import IdleScreen
from .settings import SettingsManager

logger = logging.getLogger(__name__)


class G13Daemon:
    """
    Main daemon for G13 device control.

    Coordinates:
    - Key input reading and mapping
    - LCD menu system with thumbstick navigation
    - LED backlight effects
    - Profile management
    """

    # Update intervals
    RENDER_FPS = 20
    RENDER_INTERVAL = 1.0 / RENDER_FPS

    def __init__(self):
        """Initialize daemon (does not connect to device yet)."""
        self._device = None
        self._mapper: G13Mapper | None = None
        self._lcd: G13LCD | None = None
        self._backlight: G13Backlight | None = None
        self._led_controller: LEDController | None = None
        self._screen_manager: ScreenManager | None = None
        self._input_handler: InputHandler | None = None
        self._nav_controller: NavigationController | None = None

        self._running = False
        self._render_thread: threading.Thread | None = None
        self._start_time: datetime | None = None
        self._key_count = 0

        # Profile manager
        self.profile_manager = ProfileManager()

        # Settings manager
        self.settings_manager = SettingsManager()

    @property
    def uptime(self) -> str:
        """Get daemon uptime as formatted string."""
        if not self._start_time:
            return "0:00"
        delta = datetime.now() - self._start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"

    @property
    def key_count(self) -> int:
        """Get total key press count."""
        return self._key_count

    def connect(self) -> bool:
        """
        Connect to G13 device and initialize components.

        Returns:
            True if connection successful
        """
        try:
            logger.info("Opening G13 device...")
            self._device = open_g13()
        except Exception as e:
            logger.error(f"Could not open G13: {e}")
            return False

        # Initialize hardware controllers
        self._lcd = G13LCD(self._device)
        self._backlight = G13Backlight(self._device)
        self._led_controller = LEDController(backlight=self._backlight)

        # Initialize mapper for key translation
        self._mapper = G13Mapper()

        # Initialize screen manager with LCD
        self._screen_manager = ScreenManager(lcd=self._lcd)
        self._screen_manager.led_controller = self._led_controller
        self._screen_manager.profile_manager = self.profile_manager
        self._screen_manager.settings_manager = self.settings_manager
        self._screen_manager.daemon = self

        # Create idle screen
        idle_screen = IdleScreen(
            self._screen_manager,
            profile_manager=self.profile_manager,
            settings_manager=self.settings_manager,
        )

        # Initialize navigation controller
        self._nav_controller = NavigationController(self._screen_manager, idle_screen)

        # Setup M-key profile callbacks
        self._setup_mkey_callbacks()

        # Initialize input handler
        self._input_handler = InputHandler(self._device, self._on_input_event)

        # Load default profile if available
        self._load_default_profile()

        logger.info("G13 daemon initialized")
        return True

    def _setup_mkey_callbacks(self):
        """Setup M-key callbacks for quick profile access."""
        # M1/M2/M3 show profile info toast (could be extended to switch profiles)
        self._nav_controller.set_profile_callback(
            InputEvent.BUTTON_M1,
            lambda: self._on_mkey_pressed(1),
        )
        self._nav_controller.set_profile_callback(
            InputEvent.BUTTON_M2,
            lambda: self._on_mkey_pressed(2),
        )
        self._nav_controller.set_profile_callback(
            InputEvent.BUTTON_M3,
            lambda: self._on_mkey_pressed(3),
        )

    def _on_mkey_pressed(self, m_num: int):
        """
        Handle M-key press for profile mode indication.

        Args:
            m_num: M-key number (1, 2, or 3)
        """
        profile_name = "None"
        if self.profile_manager.current_profile:
            profile_name = self.profile_manager.current_profile.name

        self.show_toast(f"M{m_num}: {profile_name}", duration=1.5)

    def _load_default_profile(self):
        """Load default/first profile if available."""
        profiles = self.profile_manager.list_profiles()
        if not profiles:
            logger.info("No profiles found")
            return

        # Try to load 'default' or 'example' profile, otherwise first available
        for name in ["default", "example", profiles[0]]:
            if name in profiles:
                try:
                    self.load_profile(name)
                    logger.info(f"Loaded profile: {name}")
                    return
                except Exception as e:
                    logger.warning(f"Could not load profile '{name}': {e}")

    def load_profile(self, name: str) -> bool:
        """
        Load a profile by name and apply its settings.

        Args:
            name: Profile name to load

        Returns:
            True if successful
        """
        try:
            profile = self.profile_manager.load_profile(name)

            # Apply backlight color
            if self._led_controller and hasattr(profile, "backlight"):
                color = profile.backlight.get("color", "#FFFFFF")
                if color.startswith("#") and len(color) == 7:
                    r = int(color[1:3], 16)
                    g = int(color[3:5], 16)
                    b = int(color[5:7], 16)
                    self._led_controller.set_color(r, g, b)

            # Update mapper with new mappings
            if self._mapper:
                from dataclasses import asdict

                self._mapper.load_profile(asdict(profile))

            # Force idle screen refresh
            if self._screen_manager and self._screen_manager.current:
                self._screen_manager.current.mark_dirty()

            return True

        except FileNotFoundError:
            logger.error(f"Profile not found: {name}")
            return False
        except Exception as e:
            logger.error(f"Error loading profile '{name}': {e}")
            return False

    def run(self):
        """
        Run the daemon main loop.

        Blocks until stopped via Ctrl+C or stop().
        """
        if not self._device:
            if not self.connect():
                sys.exit(1)

        self._running = True
        self._start_time = datetime.now()

        # Setup signal handlers
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

        # Start input handler
        self._input_handler.start()

        # Start render thread
        self._render_thread = threading.Thread(target=self._render_loop, daemon=True, name="Render")
        self._render_thread.start()

        # Force initial render
        self._screen_manager.force_render()

        logger.info("G13 daemon running. Press Ctrl+C to exit.")
        print("G13 opened. Press stick for menu. Ctrl+C to exit.")

        # Main loop - handle key mapping
        try:
            while self._running:
                try:
                    data = self._device.read(timeout_ms=100)
                    if data:
                        self._handle_raw_report(data)
                except Exception as e:
                    logger.debug(f"Read error: {e}")
                    time.sleep(0.01)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

    def stop(self):
        """Stop the daemon and clean up resources."""
        if not self._running:
            return

        logger.info("Stopping G13 daemon...")
        self._running = False

        # Stop input handler
        if self._input_handler:
            self._input_handler.stop()

        # Stop LED effects
        if self._led_controller:
            self._led_controller.stop_effect()

        # Wait for render thread
        if self._render_thread and self._render_thread.is_alive():
            self._render_thread.join(timeout=1.0)

        # Close mapper
        if self._mapper:
            self._mapper.close()

        # Clear LCD
        if self._lcd:
            try:
                self._lcd.clear()
            except Exception:
                pass

        # Close device
        if self._device:
            try:
                self._device.close()
            except Exception:
                pass

        logger.info("G13 daemon stopped")
        print("\nG13 daemon stopped.")

    def _handle_signal(self, signum, frame):
        """Handle shutdown signals."""
        self._running = False

    def _on_input_event(self, event: InputEvent):
        """
        Handle input events from InputHandler.

        Routes events to navigation controller for menu handling.

        Args:
            event: Input event
        """
        if self._nav_controller:
            self._nav_controller.on_input(event)

    def _handle_raw_report(self, data: bytes):
        """
        Handle raw HID report for key mapping.

        Passes report to mapper for key translation.

        Args:
            data: Raw HID report bytes
        """
        if self._mapper:
            # Track key presses (rough count based on mapper activity)
            self._mapper.handle_raw_report(data)
            self._key_count += 1

    def _render_loop(self):
        """Background thread for LCD rendering."""
        last_update = time.time()

        while self._running:
            try:
                now = time.time()
                dt = now - last_update
                last_update = now

                # Update screens
                if self._screen_manager:
                    self._screen_manager.update(dt)
                    self._screen_manager.render()

                # Sleep for target frame time
                elapsed = time.time() - now
                sleep_time = max(0, self.RENDER_INTERVAL - elapsed)
                time.sleep(sleep_time)

            except Exception as e:
                logger.error(f"Render error: {e}")
                time.sleep(self.RENDER_INTERVAL)

    def set_backlight_color(self, r: int, g: int, b: int):
        """
        Set backlight color.

        Args:
            r: Red (0-255)
            g: Green (0-255)
            b: Blue (0-255)
        """
        if self._led_controller:
            self._led_controller.set_color(r, g, b)

    def show_toast(self, message: str, duration: float = 2.0):
        """
        Show a toast notification on LCD.

        Args:
            message: Message to display
            duration: Display duration in seconds
        """
        if self._nav_controller:
            self._nav_controller.show_toast(message, duration)


def main():
    """Command-line entry point."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    daemon = G13Daemon()
    daemon.run()


if __name__ == "__main__":
    main()
