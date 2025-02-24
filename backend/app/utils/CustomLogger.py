import logging
import os


class CustomLogger:

    def __init__(self, log_directory_path: str, log_file_name: str, logging_level: int):
        self.logging_level = logging_level
        self.log_directory_path = log_directory_path
        self.log_file_name = log_file_name
        self.logger = logging.getLogger(__name__)  # Initialize the logger instance
        self._setup()

    def _setup(self):
        os.makedirs(self.log_directory_path, exist_ok=True)
        log_file = os.path.join(self.log_directory_path, self.log_file_name)

        # Set up the log file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(self.logging_level)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        # Set up console handler for debugging
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.logging_level)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # Set the logging level of the logger
        self.logger.setLevel(self.logging_level)  # Use the passed logging level, not hardcoded INFO

    def get_logger(self):
        return self.logger
