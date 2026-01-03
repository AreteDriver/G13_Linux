"""Tests for G13 profile manager."""

import pytest
import tempfile
from pathlib import Path
from g13_ops.gui.models.profile_manager import ProfileManager, ProfileData


class TestProfileData:
    """Test ProfileData dataclass."""

    def test_create_minimal_profile(self):
        """Create profile with just a name."""
        profile = ProfileData(name="Test")

        assert profile.name == "Test"
        assert profile.description == ""
        assert profile.version == "0.1.0"
        assert profile.mappings == {}

    def test_create_full_profile(self):
        """Create profile with all fields."""
        profile = ProfileData(
            name="Full Test",
            description="A test profile",
            version="1.0.0",
            mappings={"G1": "KEY_A"},
            lcd={"enabled": True, "default_text": "Hello"},
            backlight={"color": "#FF0000", "brightness": 50},
            joystick={"mode": "mouse"},
        )

        assert profile.name == "Full Test"
        assert profile.mappings == {"G1": "KEY_A"}
        assert profile.joystick == {"mode": "mouse"}


class TestProfileManager:
    """Test ProfileManager CRUD operations."""

    @pytest.fixture
    def temp_profiles_dir(self):
        """Create temporary profiles directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def manager(self, temp_profiles_dir):
        """Create ProfileManager with temp directory."""
        return ProfileManager(temp_profiles_dir)

    def test_list_empty_profiles(self, manager):
        """List profiles when none exist."""
        profiles = manager.list_profiles()
        assert profiles == []

    def test_create_profile(self, manager):
        """Create new profile with defaults."""
        profile = manager.create_profile("New Profile")

        assert profile.name == "New Profile"
        assert "G1" in profile.mappings
        assert "G22" in profile.mappings
        assert "M1" in profile.mappings

    def test_save_and_load_profile(self, manager):
        """Save profile and load it back."""
        profile = ProfileData(
            name="Test Save",
            description="Testing save/load",
            mappings={"G1": "KEY_F1", "G2": {"keys": ["KEY_LEFTCTRL", "KEY_C"]}},
        )

        manager.save_profile(profile, "test_save")
        loaded = manager.load_profile("test_save")

        assert loaded.name == "Test Save"
        assert loaded.mappings["G1"] == "KEY_F1"
        assert loaded.mappings["G2"] == {"keys": ["KEY_LEFTCTRL", "KEY_C"]}

    def test_list_profiles_after_save(self, manager):
        """List includes saved profiles."""
        profile = ProfileData(name="Listed")
        manager.save_profile(profile, "listed_profile")

        profiles = manager.list_profiles()

        assert "listed_profile" in profiles

    def test_load_nonexistent_raises(self, manager):
        """Loading nonexistent profile raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            manager.load_profile("does_not_exist")

    def test_delete_profile(self, manager):
        """Delete removes profile file."""
        profile = ProfileData(name="To Delete")
        manager.save_profile(profile, "to_delete")

        assert "to_delete" in manager.list_profiles()

        manager.delete_profile("to_delete")

        assert "to_delete" not in manager.list_profiles()

    def test_delete_nonexistent_raises(self, manager):
        """Deleting nonexistent profile raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            manager.delete_profile("ghost")

    def test_profile_exists(self, manager):
        """Check profile existence."""
        assert not manager.profile_exists("nope")

        profile = ProfileData(name="Exists")
        manager.save_profile(profile, "exists_test")

        assert manager.profile_exists("exists_test")

    def test_current_profile_tracking(self, manager):
        """Current profile is tracked after load."""
        profile = ProfileData(name="Current")
        manager.save_profile(profile, "current")

        assert (
            manager.current_profile is None or manager.current_profile.name == "Current"
        )

        manager.load_profile("current")
        assert manager.current_profile.name == "Current"

    def test_delete_clears_current_if_same(self, manager):
        """Deleting current profile clears it."""
        profile = ProfileData(name="deletable")  # Name matches file name
        manager.save_profile(profile, "deletable")
        manager.load_profile("deletable")

        manager.delete_profile("deletable")

        assert manager.current_profile is None


class TestProfileValidation:
    """Test profile JSON validation."""

    @pytest.fixture
    def temp_profiles_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_load_invalid_json_raises(self, temp_profiles_dir):
        """Invalid JSON raises ValueError."""
        manager = ProfileManager(temp_profiles_dir)
        path = Path(temp_profiles_dir) / "bad.json"
        path.write_text("{ not valid json")

        with pytest.raises(ValueError):
            manager.load_profile("bad")

    def test_load_missing_fields_uses_defaults(self, temp_profiles_dir):
        """Profile with missing fields uses defaults."""
        manager = ProfileManager(temp_profiles_dir)
        path = Path(temp_profiles_dir) / "minimal.json"
        path.write_text('{"name": "Minimal"}')

        profile = manager.load_profile("minimal")

        assert profile.name == "Minimal"
        assert profile.description == ""
        assert profile.mappings == {}
