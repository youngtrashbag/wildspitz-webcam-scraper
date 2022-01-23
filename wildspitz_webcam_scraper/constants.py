from datetime import datetime

WEBCAMS = {
    'wildspitz': 'https://storage.roundshot.com/5595515f75aba9.83008277',
    'rigi': 'https://storage.roundshot.com/5c1a1db365b684.49402499',
}

QUALITIES = ['full', 'default', 'half', 'quarter', 'eight']

NOW = datetime.now(tz=None).replace(second=0, microsecond=0)
