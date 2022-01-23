"""
Webcam Scraper

Usage:
    scraper.py
    scraper.py [-w WEBCAM]
    scraper.py [-q QUALITY]
    scraper.py [-t BEGIN]
    scraper.py [-t BEGIN -l END]
    scraper.py [-t BEGIN -l END -i INTERVAL]
    scraper.py [-w WEBCAM -q QUALITY -t BEGIN -l END -i INTERVAL]

Options:
-h, --help            help

-w, --webcam          Select either 'wildspitz' or 'rigi' webcam
-q, --quality         Quality of the Image (full, default, half, quarter, eight)

-t, --time            The time the image was taken (will only save 1 image)
-b, --begin           Time of the image you want to download
-l, --last            Last image you want to download
-i, --interval        Interval in minute steps (min. 10 min, and can only be increased in 10 min steps)
"""
from typing import List
from datetime import timedelta

from docopt import docopt

from wildspitz_webcam_scraper.scraper.request import create_url, ThreadedFetcher
from wildspitz_webcam_scraper.constants import WEBCAMS
from wildspitz_webcam_scraper.args import parse_args


def main():
    # argument parsing
    args = docopt(__doc__, help=True)
    from pprint import pprint
    pprint(args)
    args = parse_args(args)
    pprint(args)
    #args = parse_args(docopt(__doc__, help=True))

    # max 3 threads at a time
    active_threads: List = []
    webcam_time = args['BEGIN']
    while webcam_time < args['END']:
        if len(active_threads) < 3:
            t = ThreadedFetcher(
                create_url(WEBCAMS[args['WEBCAM']], webcam_time, args['QUALITY']), webcam_time, args['WEBCAM']
            )
            t.start()
            webcam_time += timedelta(minutes=args['INTERVAL'])
            active_threads.append(t)
        else:
            active_threads[0].join()
            active_threads.pop(0)


if __name__ == '__main__':
    main()
