from threading import Thread

from requests import get

from datetime import datetime
from os import makedirs
from pathlib import Path
from shutil import copyfileobj


# url is formatted as follows
# https://storage.roundshot.com/5595515f75aba9.83008277/2021-10-11/10-10-00/2021-10-11-10-10-00_full.jpg
def create_url(pre_url: str, dt: datetime, quality: str):
    date_fragment = f'{dt.year}-{dt.month:02}-{dt.day:02}'
    time_fragment = f'{dt.hour:02}-{dt.minute:02}-00'

    # stitching the url together
    # of course, we also want the highest resolution
    full_url = f'{pre_url}/{date_fragment}/{time_fragment}/{date_fragment}-{time_fragment}_{quality}.jpg'

    return full_url


class ThreadedFetcher(Thread):
    def __init__(self, url: str, time: datetime, webcam):
        Thread.__init__(self, name='ThreadedFetcher')
        self.time = time
        self.url = url
        self.webcam = webcam

    def run(self) -> None:
        path = Path(f'{self.time.year}-{self.time.month}') / Path(str(self.time.day) / Path(self.webcam))
        makedirs(path, exist_ok=True)

        try:
            response = get(self.url, stream=True)

            print(f'Saving Image from {self.time} under {path}.')
            img_path = path / Path(f'{self.time.hour:02}-{self.time.minute:02}.jpg')

            with open(img_path, mode="wb") as img:
                copyfileobj(response.raw, img)

            print(f'Successfully saved Image in \'{img_path}\'.')
        except Exception as e:
            print(f'Could not save Image from {self.time}.\n{e}')
