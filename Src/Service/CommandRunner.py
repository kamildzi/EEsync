#!/usr/bin/env python3

import subprocess
from sys import getdefaultencoding
from os import environ


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

    @staticmethod
    def os_exec(command: list) -> subprocess.CompletedProcess:
        """
        A runner method. Throws exception when returncode is not 0.
        """
        process_env = dict(environ)
        process_env['LC_ALL'] = 'C'
        command_result = subprocess.run(
            command,
            capture_output=True,
            encoding=getdefaultencoding(),
            env=process_env
        )

        if command_result.returncode != 0:
            raise Exception(f"Error: Failed to run: {command} "
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

    def run(self, *args):
        """
        Implementation of the binary usage.
        """
        print(f" (( {self.__class__} Not implemented! )) ")
