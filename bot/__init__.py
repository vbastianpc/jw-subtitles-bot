import logging
import datetime
import pytz
import os


TOKEN = os.getenv('TOKEN_JWSUBS')
DEV = os.getenv('DEV')

class Formatter(logging.Formatter):
    """override logging.Formatter to use an aware datetime object"""
    def converter(self, timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp)
        tzinfo = pytz.timezone('UTC')
        return tzinfo.localize(dt)

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created).astimezone(tz=pytz.timezone('America/Santiago'))
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            s = dt.isoformat(timespec='seconds')
        return s

def create_logger(name, fmt=None, datefmt=None):
    logger = logging.getLogger(name)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(Formatter(fmt or '%(asctime)s - %(name)s - %(funcName)s - %(message)s', datefmt or "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    return logger
