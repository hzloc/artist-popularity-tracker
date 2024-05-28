import logging


class ApiFactory:
    def __init__(self, logger: logging.Logger):
        """

        Args:
            logger (logging.Logger): Logger for streaming logs to console
        """
        self.log = logger
        pass

    def retrieve_data(self):
        """
        is used to gather data from API endpoints
        Returns:

        """
        raise NotImplementedError("Method must be implemented")