from datetime import datetime
from typing import Optional

from requests import get, Response


# url is formatted as follows
# https://storage.roundshot.com/5595515f75aba9.83008277/2021-10-11/10-10-00/2021-10-11-10-10-00_full.jpg
def create_url(dt: datetime):
    pre_url = 'https://storage.roundshot.com/5595515f75aba9.83008277'
    date_fragment = f'{dt.year}-{dt.month:02}-{dt.day:02}'
    time_fragment = f'{dt.hour:02}-{dt.minute:02}-00'

    # stitching the url together
    # of course, we also want the highest resolution
    full_url = f'{pre_url}/{date_fragment}/{time_fragment}/{date_fragment}-{time_fragment}_full.jpg'

    return full_url


def get_image(url: str) -> Optional[Response]:
    res = get(url, stream=True)

    if res.status_code != 200:
        return None

    return res
