"""
Wildspitz Webcam Scraper

Usage:
    scraper.py
    scraper.py [-b BEGIN]
    scraper.py [-b BEGIN -e END]
    scraper.py [-b BEGIN -e END -i INTERVAL]

Options:
-h, --help            help

-b, --begin           First image you want to download (hh-mm) or (YYYY-MM-DD_hh-mm)
-e, --end             Last image you want to download (hh-mm) or (YYYY-MM-DD_hh-mm)
-i, --interval        Interval in minute steps (min. 10 min, and can only be increased in 10 min steps)
"""
import sys
from datetime import datetime, timedelta

from docopt import docopt

from scraper.file import create_folders, save_image
from scraper.request import create_url, get_image


def main():
    # argument parsing
    args = docopt(__doc__, help=True)
    short_time_format = "%H-%M"
    time_format = "%Y-%m-%d_%H-%M"

    start = datetime.now()
    end = datetime.now()
    interval = 10

    if args['--begin']:
        try:
            if len(args['BEGIN']) > 5:
                start = datetime.strptime(args['BEGIN'], time_format)
            else:
                start = datetime.strptime(args['BEGIN'], short_time_format)
        except ValueError:
            print('Start parameter did not contain correct date format')

    if args['--end']:
        try:
            if len(args['END']) > 5:
                start = datetime.strptime(args['END'], time_format)
            else:
                start = datetime.strptime(args['END'], short_time_format)
        except ValueError:
            print('End parameter did not contain correct date format')

    if args['--interval']:
        interval = int(args['INTERVAL'])
        if interval == 0:
            raise ValueError('Interval must at least be 10 minutes')
        elif interval % 10 > 0:
            raise ValueError('Interval can only be a value divisible by 10')

    start = start.replace(minute=start.minute - (start.minute % 10),
                          second=0,
                          microsecond=0)

    while start < end:
        url = create_url(start)

        if (res := get_image(url)) is not None:
            path = create_folders(start)

            print(f'Saving Image from {start} under {path}.')
            save_image(res, path, start)
        else:
            print(f'Could not save Image from {start}.')
            sys.exit()

        start += timedelta(minutes=interval)


if __name__ == '__main__':
    main()
