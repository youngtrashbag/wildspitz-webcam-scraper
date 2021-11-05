from datetime import datetime
from os import makedirs
from pathlib import Path
from shutil import copyfileobj

from requests import Response


def create_folders(dt: datetime) -> Path:
    p = Path(f"{dt.year}-{dt.month}") / Path(str(dt.day))
    makedirs(p, exist_ok=True)

    return p


def save_image(res: Response, path: Path, dt: datetime):
    img_path = Path(path / f"{dt.hour}-{dt.minute}.jpg")

    with open(img_path, mode="wb") as img:
        copyfileobj(res.raw, img)

    print(f"Successfully saved Image in '{img_path}'.")
