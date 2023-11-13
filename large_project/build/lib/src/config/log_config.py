import logging
from logging.handlers import RotatingFileHandler
import os
import gzip

class MyLogger:
    def __init__(self, log_file, log_level=logging.INFO, max_file_size=1024, backup_count=3, max_log_files=5, compress_after=3):
        self.log_file = log_file
        self.max_log_files = max_log_files
        self.compress_after = compress_after

        # Create a logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # Create a RotatingFileHandler and set the log level, max file size, and backup count
        file_handler = RotatingFileHandler(log_file, maxBytes=max_file_size, backupCount=backup_count, mode='a')
        file_handler.setLevel(log_level)

        # Create a console handler and set the log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # Define the log message format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # Clean up old log files and compress them
        self.cleanup_and_compress_log_files()

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def cleanup_and_compress_log_files(self):
        if self.max_log_files <= 0:
            return

        log_files = [self.log_file] + [f"{self.log_file}.{i}" for i in range(1, self.max_log_files + 1)]

        # Compress log files that exceed the specified limit
        for i in range(self.compress_after, len(log_files)):
            if os.path.exists(log_files[i]):
                with open(log_files[i], 'rb') as log_file:
                    with gzip.open(log_files[i] + '.gz', 'wb') as compressed_file:
                        compressed_file.writelines(log_file)
                os.remove(log_files[i])


        # Clean up any excess log files
        for file in log_files[self.max_log_files:]:
            print(file)
            if os.path.exists(file):
                os.remove(file)

if __name__ == '__main__':
    logger = MyLogger('my_log.log', max_file_size=1024, backup_count=5, max_log_files=5, compress_after=1)

    for i in range(1, 9):
        logger.log_info("This is an information message." +str(i))
        logger.log_warning("This is a warning message." +str(i))
        logger.log_error("This is an error message." +str(i))

    
