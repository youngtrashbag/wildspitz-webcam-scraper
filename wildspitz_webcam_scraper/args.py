from typing import Dict
from datetime import datetime

from wildspitz_webcam_scraper.constants import WEBCAMS, QUALITIES, NOW


DEFAULTS = {
    'BEGIN': NOW,
    'END': NOW,
    'INTERVAL': 10,
    'WEBCAM': 'wildspitz',
    'QUALITY': 'default',
}

TIME_FORMATS = [
    '%H-%M',
    '%H:%M',

    '%d_%H-%M',
    '%d_%H-%M',

    '%m/%d_%H-%M',
    '%m/%d_%H-%M',

    '%Y-%m-%d_%H-%M',
    '%Y/%m/%d_%H:%M',
]


def parse_args(docopt_args: Dict) -> Dict:
    args = DEFAULTS

    if docopt_args['--time']:
        args['BEGIN'] = _process_time('--time', docopt_args['BEGIN'], args['BEGIN'])
    if docopt_args['--last']:
        args['END'] = _process_time('--last', docopt_args['END'], args['END'])

    if docopt_args['--interval']:
        interval = int(args['INTERVAL'])
        if interval == 0:
            raise ValueError('--interval: Interval must at least be 10 minutes')
        elif interval % 10 > 0:
            raise ValueError('--interval: Interval can only be a value divisible by 10')

    if docopt_args['--webcam']:
        webcam_name = str(docopt_args['WEBCAM']).lower()
        if webcam_name not in WEBCAMS:
            raise ValueError('--webcam: No valid Webcam was selected')

        args['WEBCAM'] = webcam_name

    if docopt_args['--quality']:
        quality = str(docopt_args['QUALITY']).lower()
        if quality not in QUALITIES:
            raise ValueError(f'--quality: {args["QUALITY"]} is not a valid quality')

        args['QUALITY'] = quality

    return args


def _parse_time(raw_time: str) -> datetime:
    time = None

    for time_format in TIME_FORMATS:
        try:
            time = datetime.strptime(raw_time, time_format)
        except ValueError as e:
            continue
        if time:
            break

    if time is None:
        raise ValueError('Datetime not in correct format')

    return time


def _process_time(key: str, raw_time: str, time_in: datetime) -> datetime:
    # default datetime
    d_dt = datetime(1900, 1, 1)

    try:
        time = _parse_time(raw_time)
    except Exception as e:
        print(f'{key}: {e}')

    # TODO: fix this, it does not work yet
    # TODO: might cause bug on january 1st
    time_in.replace(year=time.year) if time.year != d_dt.year else None
    time_in.replace(month=time.month) if time.month != d_dt.month else None
    time_in.replace(day=time.day) if time.day != d_dt.day else None
    time_in.replace(hour=time.hour) if time.hour != d_dt.hour else None
    time_in = time_in.replace(minute=time.minute) if time.minute != d_dt.minute else None

    return time_in
