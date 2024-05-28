import logging
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
    except FileNotFoundError as err:
        log.error(f"{file_path} does not exists!")
        raise f"{file_path} does not exists!"

    return file_content
