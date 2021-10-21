from datetime import datetime

from scraper.file import create_folders, save_image
from scraper.request import create_url, get_image
from scraper.time import normalize_minute, advance_minute

from arg_parser import init_parser


def main():
    # argument parsing
    start, end, interval = init_parser()

    if start is None:
        start = datetime.now()

    if end is None:
        end = datetime.now()

    if interval is not None:
        interval = interval * 10
    else:
        interval = 10

    start = normalize_minute(start)

    url = create_url(start)

    while start < end:
        if (res := get_image(url)) is not None:
            path = create_folders(start)

            save_image(res, path, start.minute)
        else:
            print(f"Image from {start} could not be fetched.\nTrying last Image.")

        start = advance_minute(start, interval)


if __name__ == "__main__":
    main()
