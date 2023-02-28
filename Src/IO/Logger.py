from datetime import datetime
from os import getcwd
from os.path import isdir, isfile

import GeneralSettings


class Logger:
    """
    The logger class.
    """
    __start_date = None
    __log_dir = None
    __log_file_is_ready: bool = False

    @classmethod
    def init(cls):
        """
        Initialize the logger object.
        """
        # set the date
        cls.__start_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # set the log directory
        default_logs_directory: str = getcwd() + "/SavedLogs"
        if GeneralSettings.logger["custom_log_dir_path"] != "":
            cls.__log_dir = GeneralSettings.logger["custom_log_dir_path"]
        else:
            cls.__log_dir = default_logs_directory

    @classmethod
    def get_log_path_dir(cls):
        """
        Returns the application log directory.
        """
        return cls.__log_dir

    @classmethod
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
        format_text += str(f"\n{text}")
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
            case "stdout_file":
                cls.__handle_file(text)
                print(text)
            case "none":
                pass
            case _:
                raise SystemExit(f"Error! Wrong logger type: {log_method}")

    @classmethod
    def __prepare_file_name_and_path(cls) -> tuple:
        """
        Returns the file_name and save_path.
        """
        file_name = f"eesync_{cls.__start_date}"
        save_path = f"{cls.__log_dir}/{file_name}.log"
        return file_name, save_path

    @classmethod
    def __handle_file(cls, text):
        """
        Writes to a file.
        """
        if not cls.__log_file_is_ready:
            cls.__init_log_file()
        file_name, save_path = cls.__prepare_file_name_and_path()

        # file validation
        if not isdir(cls.__log_dir):
            raise SystemExit(f"Error! Wrong logs directory (not a directory): {cls.__log_dir}")
        if not isfile(save_path):
            raise SystemExit(f"Error! Tried to log to a file, but the file is gone: {save_path}")

        # save the file - append mode
        with open(save_path, 'a') as file:
            file.write(f"\n{text}\n")

    @classmethod
    def __init_log_file(cls):
        """
        Prepares the log file to use.
        """
        if cls.__log_file_is_ready:
            raise SystemExit("Internal Error! Log file already exists! Tried to initialize twice?")
        file_name, save_path = cls.__prepare_file_name_and_path()

        # file validation
        if not isdir(cls.__log_dir):
            raise SystemExit(f"Error! Wrong logs directory (not a directory): {cls.__log_dir}")
        if isfile(save_path):
            raise SystemExit(f"Error! Tried to log to a new file, but the file already exists: {save_path}")

        # create the file and set the marker-flag
        with open(save_path, 'w'):
            pass
        cls.__log_file_is_ready = True
