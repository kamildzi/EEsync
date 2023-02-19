import atexit
import subprocess
from os import environ
from sys import getdefaultencoding

import GeneralSettings
from Src.IO.UserInputConsole import UserInputConsole


class CommandRunner:
    """
    OS command runner class.
    """

    binary_name: str = None
    """External binary name."""

    binary_path: str = None
    """Full binary path - should be auto-set on init."""

    accepted_version: tuple = None
    """Minimal accepted version."""

    detected_version: tuple = None
    """Actual binary version."""

    def __init__(self):
        """
        Initialize the module.
        """
        self.version_detect()
        atexit.register(self.cleanup)

    @staticmethod
    def os_exec(command: list, confirmation_required: bool = False, silent: bool = False
                ) -> subprocess.CompletedProcess:
        """
        A runner method. Throws exception when returncode is not 0.
        :param command: Command and the parameters in the form of a list.
        :param confirmation_required: bool value, False by default. Decide if we should ask user for the confirmation.
        :param silent: bool value, False by default. Allows to suppress printing the binary name that gets executed.
        :return: CompletedProcess object.
        """
        process_env = dict(environ)
        process_env['LC_ALL'] = 'C'

        if confirmation_required and GeneralSettings.runner["confirm_os_commands"]:
            print("About to execute the command: \n"
                  + ' '.join(command)
                  + "\nPlease confirm.")
            user_confirmed = UserInputConsole.read_true_or_false()
        else:
            user_confirmed = True

        if user_confirmed:
            if not silent:
                print(f"( Running: {command[0]} ... )")
            command_result = subprocess.run(
                command,
                capture_output=True,
                encoding=getdefaultencoding(),
                env=process_env
            )
        else:
            raise SystemExit("Aborted.")

        if command_result.returncode != 0:
            raise SystemExit(f"Error: Failed to run: {command} "
                             + f"\nDetails: \nSTDOUT: {command_result.stdout}\nSTDERR: {command_result.stderr}\n")
        return command_result

    def version_check(self):
        """
        Prints info about detected binary version.
        Validates the version and throws an exception if it is not correct.
        """
        print_detected_version = '.'.join(map(str, self.detected_version))
        print_accepted_version = '.'.join(map(str, self.accepted_version))

        print(f"'{self.binary_path}' - version: {print_detected_version}")

        if self.detected_version < self.accepted_version:
            print(f" ! NOTE: {print_detected_version} is lower than accepted minimal version "
                  + f"({print_accepted_version})!\n"
                  + " ! Do you wish to ignore this and continue?")
            user_acceptance = UserInputConsole.read_true_or_false()
            if user_acceptance:
                print("Continuing. \n"
                      + " ! Please note that unsupported version might cause undefined behavior.\n"
                      + " ! It is advised to do some testing before working with important data.")
            else:
                raise SystemExit("Aborted by user.")

    def cleanup(self):
        """
        Post-run cleanups. This method will be called automatically at the end of execution.
        """
        pass

    def version_detect(self):
        """
        Detects the binary's version and pre-sets required variables.
        """
        raise Exception(f" (( {self.__class__} Not implemented! )) ")

    def run(self, *args):
        """
        Implementation of the binary usage.
        """
        raise Exception(f" (( {self.__class__} Not implemented! )) ")
