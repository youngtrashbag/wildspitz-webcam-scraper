"""
Webcam Scraper

Usage:
    scraper.py
    scraper.py [-w WEBCAM]
    scraper.py [-q QUALITY]
    scraper.py [-b BEGIN]
    scraper.py [-b BEGIN -e END]
    scraper.py [-b BEGIN -e END -i INTERVAL]
    scraper.py [-w WEBCAM -q QUALITY -b BEGIN -e END -i INTERVAL]

Options:
-h, --help            help

-w, --webcam          Select either 'wildspitz' or 'rigi' webcam
-q, --quality         Quality of the Image (full, default, half, quarter, eight)

-b, --begin           First image you want to download (hh-mm) or (YYYY-MM-DD_hh-mm)
-e, --end             Last image you want to download (hh-mm) or (YYYY-MM-DD_hh-mm)
-i, --interval        Interval in minute steps (min. 10 min, and can only be increased in 10 min steps)
"""
from typing import List
from datetime import datetime, timedelta

from docopt import docopt

from wildspitz_webcam_scraper.scraper.request import create_url, ThreadedFetcher
from wildspitz_webcam_scraper.constants import WEBCAMS, QUALITIES


def main():
    # argument parsing
    args = docopt(__doc__, help=True)
    short_time_format = '%H-%M'
    time_format = '%Y-%m-%d_%H-%M'

    # settings default values
    start_time = datetime.now()
    end_time = datetime.now()
    interval = 10
    webcam_link = WEBCAMS['wildspitz']
    webcam_name = 'wildspitz'

    if args['--begin']:
        try:
            if len(args['BEGIN']) > 5:
                start_time = datetime.strptime(args['BEGIN'], time_format)
            else:
                new_time = datetime.strptime(args['BEGIN'], short_time_format)
                start_time = start_time.replace(
                    hour=new_time.hour, minute=new_time.minute
                )
                # should by default only download one image
                end_time = start_time
        except ValueError:
            print('Start parameter did not contain correct date format')

    if args['--end']:
        try:
            if len(args['END']) > 5:
                start_time = datetime.strptime(args['END'], time_format)
            else:
                new_time = datetime.strptime(args['END'], short_time_format)
                end_time = end_time.replace(hour=new_time.hour, minute=new_time.minute)
        except ValueError:
            print('End parameter did not contain correct date format')

    if args['--interval']:
        interval = int(args['INTERVAL'])
        if interval == 0:
            raise ValueError('Interval must at least be 10 minutes')
        elif interval % 10 > 0:
            raise ValueError('Interval can only be a value divisible by 10')

    if args['--webcam']:
        webcam_name = str(args['WEBCAM']).lower()

        if webcam_name not in WEBCAMS:
            raise ValueError('No valid Webcam was selected')

        webcam_link = WEBCAMS[webcam_name]

    # default quality is 'default'
    quality = QUALITIES[1]
    if args['--quality']:
        if str(args['QUALITY']) in QUALITIES:
            quality = str(args['QUALITY'])

    start_time = start_time.replace(
        minute=start_time.minute - (start_time.minute % 10), second=0, microsecond=0
    )

    # max 3 threads at a time
    active_threads: List = []
    while start_time < end_time:
        if len(active_threads) < 3:
            t = ThreadedFetcher(
                create_url(webcam_link, start_time, quality), start_time, webcam_name
            )
            t.start()
            start_time += timedelta(minutes=interval)
            active_threads.append(t)
        else:
            active_threads[0].join()
            active_threads.pop(0)


if __name__ == '__main__':
    main()
