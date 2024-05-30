import logging
from abc import ABC, abstractmethod
class Transform(ABC):
    def __init__(self, log: logging.Logger):
        self.log = log

    @abstractmethod
    def transform_data(self):
        raise NotImplementedError("Needs to be implemented")