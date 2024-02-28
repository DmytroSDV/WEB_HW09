import logging
from logging.handlers import RotatingFileHandler


# logging.CRITICAL = 50
# logging.ERROR = 40
# logging.WARNING = 30
# logging.INFO = 20
# logging.DEBUG = 10
# logging.NOTSET = 0


class CustomLogger:

    def __init__(
        self,
        log_file: str,
        console_level: int = logging.DEBUG,
        file_level: int = logging.ERROR,
        logger_name: str = "custom_logger",
        file_size: int = 1024 * 1024,
        backup_count: int = 11
    ) -> None:

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(console_level)
        self.format_info = {
            logging.DEBUG: "%(levelname)s - %(message)s",
            logging.INFO: "%(message)s",
            logging.WARNING: "%(levelname)s, %(asctime)s, line - '%(lineno)d', Message - '%(message)s'",
            logging.ERROR:  "%(levelname)s, %(asctime)s, module - '%(module)s', function - '%(funcName)s', line - '%(lineno)d'. Message - '%(message)s'",
            logging.CRITICAL: "%(levelname)s, %(asctime)s,  function - '%(funcName)s', Message - '%(message)s'"
        }

        # Log for console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        console_formatter = logging.Formatter(self.format_info[logging.INFO])
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # Log for file
        file_handler = RotatingFileHandler(
            log_file, mode="a", maxBytes=file_size, backupCount=backup_count,
            encoding='utf8')
        file_handler.setLevel(file_level)
        file_formatter = logging.Formatter(
            self.format_info[logging.ERROR], "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Hooking error in handlers
        file_handler.handleError = self.handle_formatting_error
        console_handler.handleError = self.handle_formatting_error
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def handle_formatting_error(self, record):

        logging.basicConfig(level=logging.ERROR,
                            format='%(levelname)s: %(message)s')
        logging.error(
            f"while executing log command, wrong used format! {record}")

    def log(self,  message: str = "", level: int = logging.INFO) -> None:
        self.logger.log(level, message)

    def set_format(
        self,
        format_str: str,
        level: int = logging.ERROR,
        date_format: str = "%Y-%m-%d %H:%M:%S",
    ) -> None:

        try:
            for handler in self.logger.handlers:
                if handler.level == level:
                    formatter = logging.Formatter(
                        format_str, datefmt=date_format)
                    handler.setFormatter(formatter)
            self.format_info[level] = format_str

        except Exception as ex:
            self.logger.error(f"while format overriding: {ex}")


my_logger = CustomLogger("logging.log")
if __name__ == "__main__":
    my_logger.log('Hello this is custom logger!')
