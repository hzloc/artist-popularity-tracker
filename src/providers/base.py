import logging
from abc import abstractmethod

from src.extract.base import Extract
from src.transform.base import Transform


class Provider(Extract, Transform):
    """
    Providers are the source of information

    They go through extract, transformation steps
    """
    def __init__(self, log: logging.Logger):
        super().__init__(log)

    @abstractmethod
    def retrieve_data(self):
        raise NotImplementedError("Method must be implemented")

    @abstractmethod
    def transform_data(self):
        raise NotImplementedError("Method must be implemented")