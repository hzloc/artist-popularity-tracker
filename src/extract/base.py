import logging
from abc import ABC, abstractmethod


class Extract(ABC):
    def __init__(self, log: logging.Logger):
        """

        Args:
            log (logging.Logger): Logger for streaming logs to console
        """
        self.log = log
        pass

    @abstractmethod
    def retrieve_data(self):
        """
        is used to gather data from API endpoints
        Returns:

        """
        raise NotImplementedError("Method must be implemented")

