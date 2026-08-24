from datetime import UTC, datetime, time
from zoneinfo import ZoneInfo

from src.camera.schedule import parse_schedule, should_capture


class TestParseSchedule:
    def test_empty_string(self):
        assert parse_schedule("") == []

    def test_none(self):
        assert parse_schedule(None) == []

    def test_single_time(self):
        assert parse_schedule("07:00") == [time(7, 0)]

    def test_multiple_times(self):
        result = parse_schedule("07:00,12:00,23:00")
        assert result == [time(7, 0), time(12, 0), time(23, 0)]

    def test_spaces_around_entries(self):
        result = parse_schedule(" 07:00 , 12:00 , 23:00 ")
        assert result == [time(7, 0), time(12, 0), time(23, 0)]

    def test_invalid_entries_skipped(self):
        result = parse_schedule("07:00,abc,25:99,12:30")
        assert result == [time(7, 0), time(12, 30)]

    def test_duplicates_and_sorting(self):
        result = parse_schedule("12:00,07:00,12:00")
        assert result == [time(7, 0), time(12, 0)]


class TestShouldCapture:
    TZ = "America/Sao_Paulo"
    SCHED = [time(7, 0), time(12, 0), time(23, 0)]

    def _utc(self, y, m, d, hh, mm=0):
        return datetime(y, m, d, hh, mm, tzinfo=UTC)

    def test_no_schedule_means_no_capture(self):
        now = self._utc(2026, 8, 24, 15, 0)
        assert not should_capture(None, [], self.TZ, now)

    def test_never_captured_and_slot_passed(self):
        # 14h UTC = 11h BRT -> slot 07:00 BRT ja passou
        now = self._utc(2026, 8, 24, 14, 0)
        assert should_capture(None, self.SCHED, self.TZ, now)

    def test_slot_in_future_not_due(self):
        # 08h UTC = 05h BRT -> primeiro slot so as 07:00 BRT (10h UTC)
        now = self._utc(2026, 8, 24, 8, 0)
        assert not should_capture(None, self.SCHED, self.TZ, now)

    def test_already_captured_this_slot(self):
        # capturou 10h05 UTC (07:05 BRT); agora 14h UTC (11h BRT)
        last = datetime(2026, 8, 24, 10, 5)  # naive UTC
        now = self._utc(2026, 8, 24, 14, 0)
        assert not should_capture(last, self.SCHED, self.TZ, now)

    def test_captured_before_slot_is_due(self):
        # capturou ontem; hoje slot 07:00 BRT passou
        last = datetime(2026, 8, 23, 22, 0)
        now = self._utc(2026, 8, 24, 14, 0)
        assert should_capture(last, self.SCHED, self.TZ, now)

    def test_catch_up_takes_latest_missed_slot_once(self):
        # capturou 06h BRT de ontem (09h UTC); perdeu 07:00 e ja passou 12:00 BRT
        last = datetime(2026, 8, 23, 9, 0)
        now = self._utc(2026, 8, 24, 15, 30)
        assert should_capture(last, self.SCHED, self.TZ, now)

    def test_exact_slot_boundary_is_due(self):
        # agora == exatamente 10:00 UTC = 07:00 BRT
        now = self._utc(2026, 8, 24, 10, 0)
        assert should_capture(None, self.SCHED, self.TZ, now)

    def test_invalid_timezone_falls_back_to_utc(self):
        now = self._utc(2026, 8, 24, 8, 0)  # 08:00 UTC > 07:00 UTC slot
        assert should_capture(None, [time(7, 0)], "Nao/Existe", now)

    def test_utc_timezone_direct(self):
        sched = [time(9, 0)]
        now = self._utc(2026, 8, 24, 9, 1)
        assert should_capture(None, sched, "UTC", now)

    def test_last_capture_naive_treated_as_utc(self):
        tz = ZoneInfo(self.TZ)
        # capturou 07:00 BRT de hoje = 10:00 UTC; slot 12:00 BRT ainda nao chegou
        last_local = datetime(2026, 8, 24, 7, 0, tzinfo=tz)
        last_naive_utc = last_local.astimezone(UTC).replace(tzinfo=None)
        now = self._utc(2026, 8, 24, 13, 0)  # 10:00 BRT
        assert not should_capture(last_naive_utc, self.SCHED, self.TZ, now)
