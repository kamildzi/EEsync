#!/usr/bin/env python3
import os.path
import re
from Src.Common.BackupAction import BackupAction
from functools import wraps

input_caret = '> '


class UserInputConsole:
    """
    User input wrapper and validator.
    """

    @staticmethod
    def general_input_int():
        """
        General input - restricted only to integer values.
        """
        try:
            user_input = int(input(input_caret))
        except ValueError:
            print("Wrong value! Only numbers are allowed.")
            return UserInputConsole.general_input_int()
        except (KeyboardInterrupt, EOFError):
            raise SystemExit("\nInput interrupted. Terminating.")
        return user_input

    @staticmethod
    def general_input() -> str:
        """
        General input.
        """
        try:
            user_input = input(input_caret)
        except (KeyboardInterrupt, EOFError):
            raise SystemExit("\nInput interrupted. Terminating.")
        return user_input

    @staticmethod
    def read_true_or_false() -> bool:
        """
        Reads general Yes or No values.
        """
        input_regex = re.compile("(^y$|^yes$)|(^n$|^no$)", re.IGNORECASE)
        user_input = UserInputConsole.general_input()

        match = input_regex.match(user_input)
        while not match:
            print("Wrong value! Type 'y' or 'n'. ")
            user_input = UserInputConsole.general_input()
            match = input_regex.match(user_input)

        if match.groups()[0]:
            return True
        else:
            return False

    @staticmethod
    def read_config_no() -> str:
        """
        Reads proper config number from the user.
        """
        input_regex = re.compile("(^[0-9]+$)|(^n$)")
        user_input = UserInputConsole.general_input()

        while not input_regex.match(user_input):
            print("Wrong value! Try again. ")
            user_input = UserInputConsole.general_input()

        return user_input

    @staticmethod
    def read_action() -> BackupAction:
        """
        Reads the valid action (enum). Checks if the number is within the range of enum values.
        """
        user_input = UserInputConsole.general_input_int()

        valid_range: list[int] = []
        for enum in BackupAction:
            valid_range.append(enum.value)

        while user_input not in valid_range:
            print(f"Wrong value! Valid options are: {valid_range}. ")
            user_input = UserInputConsole.general_input_int()

        return BackupAction(user_input)

    @staticmethod
    def read_directory_path() -> str:
        """
        Reads the valid path to the directory.
        """
        user_input = UserInputConsole.general_input()

        while not os.path.isdir(user_input):
            print("Wrong value! Try again. ")
            user_input = UserInputConsole.general_input()

        return user_input

    @staticmethod
    def read_file_path() -> str:
        """
        Reads the valid path to the file.
        """
        user_input = UserInputConsole.general_input()

        while not os.path.isfile(user_input):
            print("Wrong value! Try again. ")
            user_input = UserInputConsole.general_input()

        return user_input
