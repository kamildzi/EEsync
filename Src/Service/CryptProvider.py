#!/usr/bin/env python3

from Src.Config.ConfigEntry import ConfigEntry
from Src.Service.CommandRunner import CommandRunner
from Src.IO.UserInputConsole import UserInputConsole
import re


class CryptProvider(CommandRunner):
    """
    Provides encryption related methods.
    """
    binary_name: str = "encfs"
    accepted_version: tuple = (1, 9, 5)

    config: ConfigEntry = None
    """Config to be set manually with `set_config()` method."""

    def __init__(self):
        """
        Detects the binary's version and pre-sets required variables.
        """

        # detect binary path
        which_result = self.os_exec(["which", self.binary_name])
        self.binary_path = str(which_result.stdout).strip()

        # detect/parse the version
        version_check_result = self.os_exec([self.binary_path, "--version"])
        result_string = str(version_check_result.stderr).strip()
        matched_string = re.search(r"^encfs\s+version\s+(\d.*\.\d)\s*$", result_string)
        if not matched_string:
            raise SystemExit(f"Error! Unmatched version string for: {self.binary_path}!\n{version_check_result}")
        version_string = matched_string.groups()[0]
        self.detected_version = tuple([
            int(num) for num in version_string.split('.')
        ])

    def set_config(self, config: ConfigEntry):
        """
        Set the config to work with.
        """
        self.config = config
        if not self.config.encfs_enabled:
            raise Exception("EncFS encryption was requested, but it is not supported disabled by the given config!")
