from datetime import datetime, timedelta


def normalize_minute(dt: datetime) -> datetime:
    # image only taken in 10 minute intervals
    return dt.replace(minute=dt.minute - (dt.minute % 10), second=0, microsecond=0)


def advance_minute(dt: datetime, minute: int) -> datetime:
    return dt + timedelta(minutes=minute)
