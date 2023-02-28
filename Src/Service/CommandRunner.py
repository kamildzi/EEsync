import atexit
import subprocess
from os import environ
from sys import getdefaultencoding

import GeneralSettings
from Src.IO.UserInputConsole import UserInputConsole
from Src.IO.Logger import Logger


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
    def os_exec(command: list, confirmation_required: bool = False, silent: bool = False, capture_output: bool = True,
                logging_enabled: bool = True) -> subprocess.CompletedProcess:
        """
        A runner method. Throws exception when returncode is not 0.
        :param command: Command and the parameters in the form of a list.
        :param confirmation_required: bool value, False by default. Decide if we should ask user for the confirmation.
        :param silent: bool value, False by default. Allows to suppress printing the binary name that gets executed.
        :param capture_output: bool value, True by default. Allows to control whether the command output is captured.
        :param logging_enabled: bool value, True by default. Allows to control whether the logging feature is enabled.
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
            if logging_enabled:
                Logger.log("Executing command: \n" + ' '.join(command))
            if not silent:
                print(f"( Running: {command[0]} ... )")
            command_result = subprocess.run(
                command,
                capture_output=capture_output,
                encoding=getdefaultencoding(),
                env=process_env
            )
        else:
            if logging_enabled:
                Logger.log("Skipped command / execution aborted: \n" + ' '.join(command))
            raise SystemExit("Aborted.")

        if command_result.returncode != 0:
            failed_msg = str(f"Error: Failed to run: {command} "
                             + f"\nDetails: \nSTDOUT: {command_result.stdout}\nSTDERR: {command_result.stderr}\n")
            if logging_enabled:
                Logger.log(failed_msg)
            raise SystemExit(failed_msg)

        return command_result

    @staticmethod
    def gen_run_report(exec_command, stdout, stderr, logging_enabled: bool = True) -> str:
        """
        Generates formatted string from command output. Useful only for the reports.
        :param exec_command: Command that you executed.
        :param stdout: Standard output from the command.
        :param stderr: Standard error output from the command.
        :param logging_enabled: Allows to pass the output (returned value) to the logger.
        :return: formatted string.
        """
        if stdout is None:
            stdout = str(f"{stdout} - no output or output disabled.\n")
        if stderr is None:
            stderr = str(f"{stderr} - no output or output disabled.\n")
        formatted_string = str(f"--- STDOUT: {exec_command}: ---\n"
                               + str(stdout)
                               + f"--- STDERR: {exec_command}: ---\n"
                               + str(stderr))
        if logging_enabled:
            Logger.log(formatted_string)
        return formatted_string

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
