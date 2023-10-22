import os
import logging
import threading

class SingletonLogger:
    _instance_lock = threading.Lock()
    _logger_instance = None
    _log_folder = os.getenv("LOG_FOLDER")

    def __new__(cls):
        with cls._instance_lock:
            if not cls._logger_instance:
                cls._logger_instance = super().__new__(cls)
                cls._logger_instance.logger = logging.getLogger(__name__)
                cls._logger_instance.logger.setLevel(logging.DEBUG)

                formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

                stream_handler = logging.StreamHandler()
                stream_handler.setFormatter(formatter)

                file_handler = logging.FileHandler(f'{cls._log_folder}/application.log')
                file_handler.setFormatter(formatter)

                cls._logger_instance.logger.addHandler(stream_handler)
                cls._logger_instance.logger.addHandler(file_handler)
                
            return cls._logger_instance

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

logger = SingletonLogger()