from datetime import datetime


def normalize_minute(dt: datetime) -> datetime:
    # image only taken in 10 minute intervals
    return dt.replace(minute=dt.minute - (dt.minute % 10))


def advance_minute(dt: datetime, minute: int) -> datetime:
    if minute / 60 > 1:
        return dt.replace(hour=round(minute / 60), minute=minute % 60)
