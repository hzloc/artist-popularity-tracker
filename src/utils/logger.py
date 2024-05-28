import logging
import sys
from typing import Union, Literal


def get_logger(name: str, level: int):
    log = logging.getLogger(name)
    log.setLevel(level)

    handler = logging.StreamHandler(stream=sys.stdout)
    log.addHandler(handler)

    return log

if __name__ == '__main__':
    log = get_logger("Log", 0)
    log.error("TEST")