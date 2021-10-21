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

parser.add_argument("-i", "--interval",
                    type=int,
                    metavar="1",
                    help="The Interval in which images should be fetched (1 -> every 10 minutes)")


def init_parser() -> (Optional[datetime], Optional[datetime], Optional[int]):
    """
    Will initialize argument parser, validate and initialize the values passed
    Start Time: first image to be saved
    End Time: last image to be saved
    Interval: the interval in which images should be requested, (1 -> every 10 minutes)
    :return: Tuple of (start_time, end_time, interval)
    """
    args = parser.parse_args()

    time_format = "%Y-%m-%d_%H-%M"

    # if no other start or end time is specified, use time now
    start = None
    end = None
    interval = 1

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

    if args.interval is not None:
        try:
            interval = int(args.interval)
        except ValueError:
            print("Interval parameter is invalid")

    # start time, end time, interval
    return (start, end, interval)
