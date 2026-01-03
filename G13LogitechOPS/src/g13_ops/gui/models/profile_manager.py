"""
Profile Manager

Manages CRUD operations for G13 button mapping profiles.
"""

import json
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass, asdict, field


@dataclass
class ProfileData:
    """
    Profile data structure matching JSON format.

    Supports two mapping formats:
    - Simple: {'G1': 'KEY_1', ...}
    - Combo:  {'G1': {'keys': ['KEY_LEFTCTRL', 'KEY_B'], 'label': '...'}, ...}
    """

    name: str
    description: str = ""
    version: str = "0.1.0"
    mappings: dict = field(default_factory=dict)  # str | dict values
    lcd: dict = field(default_factory=lambda: {"enabled": True, "default_text": ""})
    backlight: dict = field(
        default_factory=lambda: {"color": "#FFFFFF", "brightness": 100}
    )
    joystick: dict = field(default_factory=dict)  # Optional joystick config


class ProfileManager:
    """Manages profile CRUD operations"""

    def __init__(self, profiles_dir: Optional[str] = None):
        if profiles_dir is None:
            # Default to configs/profiles in project root
            project_root = Path(__file__).parent.parent.parent.parent.parent
            profiles_dir = project_root / "configs" / "profiles"

        self.profiles_dir = Path(profiles_dir)
        self.current_profile: Optional[ProfileData] = None

        # Ensure profiles directory exists
        self.profiles_dir.mkdir(parents=True, exist_ok=True)

    def list_profiles(self) -> List[str]:
        """Return list of available profile names"""
        return [p.stem for p in self.profiles_dir.glob("*.json")]

    def load_profile(self, name: str) -> ProfileData:
        """
        Load profile from JSON file

        Args:
            name: Profile name (without .json extension)

        Returns:
            Loaded ProfileData

        Raises:
            FileNotFoundError: If profile doesn't exist
            ValueError: If profile JSON is invalid
        """
        path = self.profiles_dir / f"{name}.json"

        if not path.exists():
            raise FileNotFoundError(f"Profile '{name}' not found at {path}")

        try:
            with open(path, "r") as f:
                data = json.load(f)
            profile = ProfileData(**data)
            self.current_profile = profile
            return profile
        except (json.JSONDecodeError, TypeError) as e:
            raise ValueError(f"Invalid profile JSON in '{name}': {e}")

    def save_profile(self, profile: ProfileData, name: Optional[str] = None):
        """
        Save profile to JSON file

        Args:
            profile: ProfileData to save
            name: Optional profile name (uses profile.name if not provided)
        """
        save_name = name or profile.name
        path = self.profiles_dir / f"{save_name}.json"

        with open(path, "w") as f:
            json.dump(asdict(profile), f, indent=2)

        self.current_profile = profile

    def create_profile(self, name: str) -> ProfileData:
        """
        Create new empty profile with default mappings

        Args:
            name: Profile name

        Returns:
            New ProfileData with default mappings
        """
        # Create default mappings for all buttons
        default_mappings = {}

        # G keys (G1-G22)
        for i in range(1, 23):
            default_mappings[f"G{i}"] = "KEY_RESERVED"

        # M keys (M1-M3)
        for i in range(1, 4):
            default_mappings[f"M{i}"] = "KEY_RESERVED"

        profile = ProfileData(
            name=name,
            description="",
            version="0.1.0",
            mappings=default_mappings,
            lcd={"enabled": True, "default_text": ""},
            backlight={"color": "#FFFFFF", "brightness": 100},
        )

        return profile

    def delete_profile(self, name: str):
        """
        Delete profile file

        Args:
            name: Profile name to delete

        Raises:
            FileNotFoundError: If profile doesn't exist
        """
        path = self.profiles_dir / f"{name}.json"

        if not path.exists():
            raise FileNotFoundError(f"Profile '{name}' not found")

        path.unlink()

        # Clear current profile if it was the deleted one
        if self.current_profile and self.current_profile.name == name:
            self.current_profile = None

    def profile_exists(self, name: str) -> bool:
        """Check if a profile exists"""
        path = self.profiles_dir / f"{name}.json"
        return path.exists()
