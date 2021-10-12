from typing import Optional
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()

parser.description = "Scrape Images from the Wildspitz Roundshot Camera"

parser.add_argument("-s", "--start",
                    type=str,
                    metavar="YYYY-MM-DD_hh-mm",
                    help="The DateTime where scraper should start")

parser.add_argument("-e", "--end",
                    type=str,
                    metavar="YYYY-MM-DD_hh-mm",
                    help="The DateTime where scraper should end")


def init_parser() -> (Optional[datetime], Optional[datetime], Optional[int]):
    args = parser.parse_args()

    time_format = "%Y-%m-%d_%H-%M"

    # if no other start or end time is specified, use time now
    start = None
    end = None

    if args.start is not None:
        try:
            start = datetime.strptime(args.start, time_format)
        except ValueError:
            print("Start parameter did not contain correct date format")

    if args.end is not None:
        try:
            end = datetime.strptime(args.end, time_format)
        except ValueError:
            print("End parameter did not contain correct date format")

    # start time, end time, interval
    return (start, end, None)
