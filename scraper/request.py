import os
import time
from requests import get
from pathlib import Path
from threading import Thread
from datetime import datetime
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
    def __init__(self, url: str, time: datetime, webcam: str):
        Thread.__init__(self, name='ThreadedFetcher')
        self.time = time
        self.url = url
        self.webcam = webcam
        self.quality = (self.url).split('/')[-1].split('_')[-1].split('.')[0]

    def run(self) -> None:
        # path = Path(f'{self.time.year}-{self.time.month}') / Path(
        #     str(self.time.day) / Path(self.webcam)
        # )
        path = Path(
            '{}/{}-{}/{}/{}'.format(
                self.quality,
                self.time.year,
                self.time.month,
                self.time.day,
                self.webcam,
            )
        )
        os.makedirs(path, exist_ok=True)

        try:
            img_path = path / Path(f'{self.time.hour:02}-{self.time.minute:02}.jpg')
            if os.path.exists(img_path):
                print("Skip {} (Already existed)".format(img_path))
            else:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
                }
                response = get(self.url, stream=True, headers=headers)
                if response.status_code == 200:
                    print(f'Saving Image from {self.time} under {path}.')

                    with open(img_path, mode="wb") as img:
                        copyfileobj(response.raw, img)

                    print(f'Successfully saved Image in \'{img_path}\'.')
                else:
                    print(
                        "Skip {} (status code: {})".format(
                            self.url, response.status_code
                        )
                    )
                # avoid frequent request
                time.sleep(10)
                # TODO: use scrapy or proxies to avoid status code:429
        except Exception as e:
            print(f'Could not save Image from {self.time}.\n{e}')
