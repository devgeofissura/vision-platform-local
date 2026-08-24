"""Agenda de captura diária (HH:MM) com fuso configurável."""
import logging
from datetime import UTC, datetime, time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

logger = logging.getLogger(__name__)


def parse_schedule(raw: str | None) -> list[time]:
    """Converte '07:00,12:00, 23:00' em [time(7), time(12), time(23)].

    Entradas inválidas são ignoradas com warning; vazia retorna [].
    """
    if not raw or not raw.strip():
        return []

    times: list[time] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            hh, mm = part.split(":")
            times.append(time(int(hh), int(mm)))
        except (ValueError, TypeError):
            logger.warning("Horário inválido na agenda de captura: %r", part)
    return sorted(set(times))


def should_capture(
    last_capture_utc: datetime | None,
    schedule_times: list[time],
    tz_name: str,
    now_utc: datetime | None = None,
) -> bool:
    """True se há slot agendado vencido ainda não capturado.

    Semântica de catch-up: se o serviço estava fora no horário do slot,
    captura uma única vez pelo slot mais recente já vencido.
    """
    if not schedule_times:
        return False

    now = now_utc or datetime.now(UTC)
    try:
        tz = ZoneInfo(tz_name)
    except (ZoneInfoNotFoundError, ValueError):
        logger.warning("Timezone inválida %r; usando UTC", tz_name)
        tz = ZoneInfo("UTC")

    now_local = now.replace(tzinfo=UTC).astimezone(tz)
    last_local = None
    if last_capture_utc is not None:
        last_local = last_capture_utc.replace(tzinfo=UTC).astimezone(tz)

    for slot in reversed(schedule_times):
        slot_dt = now_local.replace(hour=slot.hour, minute=slot.minute, second=0, microsecond=0)
        if slot_dt > now_local:
            continue
        if last_local is None or last_local < slot_dt:
            return True
        return False

    return False
