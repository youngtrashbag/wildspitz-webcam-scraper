from datetime import datetime

from scraper.file import create_folders, save_image
from scraper.time import normalize_minute
from scraper.request import create_url, get_image


def main():
    # no arguments, just scrape most recent image
    now = datetime.now()
    now = normalize_minute(now)

    url = create_url(now)

    if res := get_image(url) is not None:
        path = create_folders(now)

        save_image(res, path, now.minute)
    else:
        print("Latest Image could not be fetched.\nTrying last Image.")

        if now.minute - 10 < 0:
            now = now.replace(minute=50)
        else:
            now = now.replace(minute=now.minute - 10)

        url = create_url(now)

        res = get_image(url)

        path = create_folders(now)
        save_image(res, path, now.minute)


if __name__ == "__main__":
    main()
