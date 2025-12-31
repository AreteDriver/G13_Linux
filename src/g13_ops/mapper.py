from evdev import UInput, ecodes as e
from typing import Union


class G13Mapper:
    """
    G13 event mapper - converts button presses to keyboard events.

    Supports both simple keys and key combinations (e.g., Ctrl+B).
    """

    def __init__(self):
        self.ui = UInput()
        # button_id (str) -> list of evdev keycodes (for combos)
        self.button_map: dict[str, list[int]] = {}

    def close(self):
        self.ui.close()

    def load_profile(self, profile_data: dict):
        """
        Load button mappings from profile.

        Supports two formats:
        - Simple: {'G1': 'KEY_1', ...}
        - Combo:  {'G1': {'keys': ['KEY_LEFTCTRL', 'KEY_B'], 'label': '...'}, ...}
        """
        self.button_map = {}
        mappings = profile_data.get('mappings', {})

        for button_id, mapping in mappings.items():
            keycodes = self._parse_mapping(mapping)
            if keycodes:
                self.button_map[button_id] = keycodes

    def _parse_mapping(self, mapping: Union[str, dict]) -> list[int]:
        """Parse a mapping entry into a list of keycodes."""
        if isinstance(mapping, str):
            # Simple format: 'KEY_1'
            if hasattr(e, mapping):
                return [getattr(e, mapping)]
            return []

        if isinstance(mapping, dict):
            # Combo format: {'keys': ['KEY_LEFTCTRL', 'KEY_B'], ...}
            keys = mapping.get('keys', [])
            keycodes = []
            for key_name in keys:
                if hasattr(e, key_name):
                    keycodes.append(getattr(e, key_name))
            return keycodes

        return []

    def handle_button_event(self, button_id: str, is_pressed: bool):
        """
        Handle decoded button event from GUI.

        For key combinations, press all keys in order on press,
        and release all keys in reverse order on release.
        """
        if button_id not in self.button_map:
            return

        keycodes = self.button_map[button_id]
        state = 1 if is_pressed else 0

        if is_pressed:
            # Press in order (modifiers first)
            for keycode in keycodes:
                self.ui.write(e.EV_KEY, keycode, state)
        else:
            # Release in reverse order
            for keycode in reversed(keycodes):
                self.ui.write(e.EV_KEY, keycode, state)

        self.ui.syn()

    def send_key(self, keycode):
        """Emit a single key press + release."""
        self.ui.write(e.EV_KEY, keycode, 1)
        self.ui.write(e.EV_KEY, keycode, 0)
        self.ui.syn()

    def handle_raw_report(self, data: bytes | list[int]):
        """
        Given a raw G13 report (list of bytes), decode which logical button
        changed and emit the mapped key, if any.

        NOTE: This is the legacy CLI interface. The GUI uses handle_button_event instead.
        """
        # TODO: decode data -> logical_button_id
        # For now, just print for debugging
        print("RAW:", list(data))
        # Example once you know mapping:
        # button_id = decode_button(data)
        # keycode = BUTTON_TO_KEY.get(button_id)
        # if keycode:
        #     self.send_key(keycode)

