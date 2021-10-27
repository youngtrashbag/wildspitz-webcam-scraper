"""
Wildspitz Webcam Scraper

Usage:
    scraper.py
    scraper.py [-b BEGIN]
    scraper.py [-b BEGIN -e END]
    scraper.py [-b BEGIN -e END -i INTERVAL]

Options:
-h, --help            help

-b, --begin           First image you want to download (YYYY-MM-DD_hh-mm)
-e, --end             First image you want to download (YYYY-MM-DD_hh-mm)
-i, --interval        Interval in ten minute steps (1 -> 10 min)
"""
import sys
from datetime import datetime

from docopt import docopt

from scraper.file import create_folders, save_image
from scraper.request import create_url, get_image
from scraper.time import normalize_minute, advance_minute


def main():
    # argument parsing
    args = docopt(__doc__, help=True)
    time_format = "%Y-%m-%d_%H-%M"

    start = datetime.now()
    end = datetime.now()
    interval = 10

    if args["--begin"]:
        try:
            start = datetime.strptime(args["BEGIN"], time_format)
        except ValueError:
            print("Start parameter did not contain correct date format")

    if args["--end"]:
        try:
            end = datetime.strptime(args["END"], time_format)
        except ValueError:
            print("End parameter did not contain correct date format")

    if args["--interval"]:
        interval = int(args["INTERVAL"]) * 10

    start = normalize_minute(start)

    url = create_url(start)

    while start < end:
        if (res := get_image(url)) is not None:
            path = create_folders(start)

            print(f"Saving Image from {start} under {path}.")
            save_image(res, path, start)
        else:
            print(f"Could not save Image from {start}.")
            sys.exit()

        start = advance_minute(start, interval)


if __name__ == "__main__":
    main()
