from unittest.mock import patch

import pytest

from src.config.global_settings import (
    DEFAULT_SETTINGS,
    clear_cache,
    get_all_settings,
    get_setting,
    get_setting_bool,
    get_setting_float,
    get_setting_int,
    seed_default_settings,
    set_setting,
    set_settings,
)
from src.storage.models import SystemSettings
from tests.conftest import TestSession


@pytest.fixture(autouse=True)
def _gs_session():
    clear_cache()
    with patch("src.config.global_settings.SessionLocal", TestSession):
        yield
    clear_cache()


@pytest.fixture
def db():
    session = TestSession()
    yield session
    session.close()


# ── seed_default_settings ──


class TestSeedDefaults:
    def test_seeds_all_defaults(self, db):
        inserted = seed_default_settings(db=db)
        assert inserted == len(DEFAULT_SETTINGS)
        rows = db.query(SystemSettings).all()
        assert len(rows) == len(DEFAULT_SETTINGS)

    def test_seed_is_idempotent(self, db):
        seed_default_settings(db=db)
        assert seed_default_settings(db=db) == 0

    def test_seed_values_match_defaults(self, db):
        seed_default_settings(db=db)
        row = db.query(SystemSettings).filter(SystemSettings.key == "local_id").first()
        assert row.value == DEFAULT_SETTINGS["local_id"]
        assert row.description is not None

    def test_seed_preserves_modified_values(self, db):
        set_setting("capture_interval_minutes", 30, db=db)
        seed_default_settings(db=db)
        assert get_setting("capture_interval_minutes", db=db) == "30"

    def test_seed_without_db_uses_session_local(self):
        inserted = seed_default_settings()
        assert inserted == len(DEFAULT_SETTINGS)


# ── get_setting ──


class TestGetSetting:
    def test_get_from_db(self, db):
        set_setting("local_id", "sl999999", db=db)
        assert get_setting("local_id", db=db) == "sl999999"

    def test_missing_key_falls_back_to_default_settings(self, db):
        assert get_setting("mqtt_broker_host", db=db) == DEFAULT_SETTINGS["mqtt_broker_host"]

    def test_unknown_key_returns_none(self, db):
        assert get_setting("nonexistent_key", db=db) is None

    def test_unknown_key_returns_explicit_default(self, db):
        assert get_setting("nonexistent_key", default="fallback", db=db) == "fallback"

    def test_empty_password_is_valid_value(self, db):
        set_setting("camera_default_password", "", db=db)
        assert get_setting("camera_default_password", db=db) == ""


# ── typed getters ──


class TestTypedGetters:
    def test_int(self, db):
        set_setting("capture_jpeg_quality", 75, db=db)
        assert get_setting_int("capture_jpeg_quality", db=db) == 75

    def test_int_bad_value_returns_default(self, db):
        set_setting("capture_jpeg_quality", "abc", db=db)
        assert get_setting_int("capture_jpeg_quality", default=90, db=db) == 90

    def test_int_missing_key_returns_default(self, db):
        assert get_setting_int("nope", default=42, db=db) == 42

    def test_float(self, db):
        set_setting("custom_ratio", "1.5", db=db)
        assert get_setting_float("custom_ratio", db=db) == 1.5

    def test_float_bad_value(self, db):
        set_setting("custom_ratio", "not-a-number", db=db)
        assert get_setting_float("custom_ratio", default=2.0, db=db) == 2.0

    def test_bool_true_variants(self, db):
        for v in ("true", "True", "1", "yes", "on"):
            set_setting("mqtt_enabled", v, db=db)
            assert get_setting_bool("mqtt_enabled", db=db) is True

    def test_bool_false_variants(self, db):
        for v in ("false", "0", "no", "", "off"):
            set_setting("mqtt_enabled", v, db=db)
            assert get_setting_bool("mqtt_enabled", db=db) is False

    def test_bool_missing_key_returns_default(self, db):
        assert get_setting_bool("nope", default=True, db=db) is True


# ── set_setting / set_settings ──


class TestSetSetting:
    def test_insert_new_key(self, db):
        set_setting("brand_new_key", "value1", description="d", db=db)
        row = db.query(SystemSettings).filter(SystemSettings.key == "brand_new_key").first()
        assert row.value == "value1"
        assert row.description == "d"

    def test_upsert_updates_existing(self, db):
        set_setting("local_name", "First", db=db)
        set_setting("local_name", "Second", db=db)
        assert get_setting("local_name", db=db) == "Second"
        count = db.query(SystemSettings).filter(SystemSettings.key == "local_name").count()
        assert count == 1

    def test_non_string_value_coerced(self, db):
        set_setting("camera_default_channel", 3, db=db)
        assert get_setting("camera_default_channel", db=db) == "3"
        assert isinstance(get_setting("camera_default_channel", db=db), str)

    def test_none_value_becomes_empty_string(self, db):
        set_setting("some_key", None, db=db)
        assert get_setting("some_key", db=db) == ""

    def test_bulk_set_settings(self, db):
        set_settings({"a_key": "1", "b_key": "2"}, db=db)
        assert get_setting("a_key", db=db) == "1"
        assert get_setting("b_key", db=db) == "2"


# ── cache ──


class TestCache:
    def test_second_read_uses_cache(self, db):
        set_setting("cached_key", "v1", db=db)
        first = get_setting("cached_key")
        second = get_setting("cached_key")
        assert first == second == "v1"

    def test_set_invalidates_cache(self, db):
        set_setting("cached_key", "v1", db=db)
        set_setting("cached_key", "v2", db=db)
        assert get_setting("cached_key") == "v2"

    def test_clear_cache_forces_db_read(self, db):
        set_setting("cached_key", "v1", db=db)
        clear_cache()
        assert get_setting("cached_key", db=db) == "v1"


# ── get_all_settings ──


class TestGetAllSettings:
    def test_empty_db_returns_defaults(self, db):
        all_settings = get_all_settings(db=db)
        assert all_settings == DEFAULT_SETTINGS

    def test_db_overrides_defaults(self, db):
        seed_default_settings(db=db)
        set_setting("local_id", "sl000042", db=db)
        result = get_all_settings(db=db)
        assert result["local_id"] == "sl000042"
        assert len(result) == len(DEFAULT_SETTINGS)

    def test_includes_custom_keys(self, db):
        set_setting("extra_key", "x", db=db)
        result = get_all_settings(db=db)
        assert result["extra_key"] == "x"
