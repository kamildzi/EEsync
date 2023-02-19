from datetime import datetime
from os import getcwd
from os.path import isdir, isfile

import GeneralSettings


class Logger:
    """
    The logger class.
    """
    start_date = None
    log_dir = None

    @classmethod
    def init(cls):
        """
        Initialize the logger object.
        """
        # set the date
        cls.start_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # and the log directory
        default_logs_directory: str = getcwd() + "/SavedLogs"
        if GeneralSettings.logger["custom_log_dir_path"] != "":
            cls.log_dir = GeneralSettings.logger["custom_log_dir_path"]
        else:
            cls.log_dir = default_logs_directory

    def log(cls, text: str, log_level: str = None):
        """
        Save the log.
        """
        cls.__log(cls.__format_text(text, log_level))

    @classmethod
    def __format_text(cls, text: str, log_level: str):
        """
        Unifies given text to common format.
        """
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        format_text = str(f"[{current_date}]")
        if log_level:
            format_text += str(f" [{log_level}]")
        format_text += str(f" : {text}")
        return format_text

    @classmethod
    def __log(cls, text: str):
        """
        Internal log proxy.
        """
        log_method = GeneralSettings.logger["log_method"]
        match log_method:
            case "stdout":
                print(text)
            case "file":
                cls.__handle_file(text)
                pass
            case "none":
                pass
            case _:
                raise SystemExit(f"Error! Wrong logger type: {log_method}")

    @classmethod
    def __handle_file(cls, text):
        """
        Writes to a file.
        """

        # prepare file name
        file_name = f"eesync_{cls.start_date}"
        save_path = f"{cls.log_dir}/{file_name}.log"

        # a little of validation
        if not isdir(cls.log_dir):
            raise SystemExit(f"Error! Wrong logs directory (not a directory): f{cls.log_dir}")
        if isfile(save_path):
            raise SystemExit(f"Error! Tried to log to a file, but the file already exists: {save_path}")

        # save the file
        with open(save_path, 'w') as file:
            file.write(text)
