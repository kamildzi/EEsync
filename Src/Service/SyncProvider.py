#!/usr/bin/env python3

import re

from Src.Config.ConfigEntry import ConfigEntry
from Src.Service.CommandRunner import CommandRunner


class SyncProvider(CommandRunner):
    """
    Provides file-sync related methods.
    """
    binary_name: str = "rsync"
    accepted_version: tuple = (3, 2, 7)

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
        result_string = str(version_check_result.stdout).strip()
        matched_string = re.search(r"^rsync\s+version\s+(\d.*\.\d)\s+", result_string)
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
