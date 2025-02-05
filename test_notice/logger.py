import logging
import sys


class LoggerClient():
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

        formatter = logging.Formatter(fmt="[%(asctime)s] - [%(levelname)s] - %(name)s >> %(message)s")

        stream_handler = logging.StreamHandler(sys.stdout)
        file_handler = logging.FileHandler('app.log')

        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        self.logger.handlers = [stream_handler, file_handler]

        self.logger.setLevel(logging.INFO)
