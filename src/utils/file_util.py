import logging
import os
from pathlib import Path
from typing import Any, Union

from src.utils.logger import get_logger

log = get_logger("File Utils Logger", level=logging.ERROR)


def open_file(file_path: Union[str, Path]) -> Any:
    """

    Args:
        file_path (str): Location of the file in system

    Returns: the content of the file being read

    """
    try:
        with open(file_path) as f:
            file_content = f.read()
    except Exception as err:
        log.error(f"{file_path} does not exists!")
        log.error(f"{os.listdir()}")
        raise BaseException(f"{err}")
    return file_content
