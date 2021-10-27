from datetime import datetime


def normalize_minute(dt: datetime) -> datetime:
    # image only taken in 10 minute intervals
    return dt.replace(minute=dt.minute - (dt.minute % 10), second=0, microsecond=0)


def advance_minute(dt: datetime, minute: int) -> datetime:
    if minute / 60 > 1:
        return dt.replace(hour=round(minute / 60), minute=minute % 60)
    else:
        return dt.replace(minute=minute)
