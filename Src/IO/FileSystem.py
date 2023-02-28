import os

from Src.IO.Logger import Logger
from Src.IO.UserInputConsole import UserInputConsole


class FileSystem:
    """
    File System (OS) level methods.
    """

    @classmethod
    def require_created_directory(cls, directory_path: str, interactive: bool = True):
        """
        Checks if the directory exists.\n
        If it does - the method does not do anything.\n
        Otherwise - create_dir_interactive() or create_dir() is triggered (depending on `interactive` param value).
        :param interactive: Boolean, True by default. Controls if the directory should be created in interactive mode.
        :param directory_path: The path that should be created.
        """
        if not os.path.isdir(directory_path):
            if interactive:
                cls.create_dir_interactive(directory_path)
            else:
                cls.create_dir(directory_path)

    @classmethod
    def create_dir_interactive(cls, directory_path: str):
        """
        Creates a new directory (only if the user confirms).
        :param directory_path: The path that should be created.
        """
        print("About to create a new directory: \n"
              + directory_path
              + "\nPlease confirm. [y/n] ")

        create_dir_confirmed = UserInputConsole.read_true_or_false()
        if create_dir_confirmed:
            cls.create_dir(directory_path)

    @classmethod
    def create_dir(cls, directory_path: str):
        """
        Creates a new directory (without user confirmation).
        :param directory_path: The path that should be created.
        """
        if os.path.exists(directory_path):
            raise Exception("Given path already exists! The path: \n" + directory_path)
        else:
            os.makedirs(directory_path)
            Logger.log("Created a new directory at: \n" + directory_path)
