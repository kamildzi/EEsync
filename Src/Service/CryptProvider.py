#!/usr/bin/env python3

import re
from functools import wraps

from Src.Common.BackupAction import BackupAction
from Src.Config.ConfigEntry import ConfigEntry
from Src.IO.Logger import Logger
from Src.Service.CommandRunner import CommandRunner


def validate_config(method):
    """
    Continue only if the config is valid and encfs is enabled.
    """

    @wraps(method)
    def __wrapper(self, *method_args, **method_kwargs):
        if self.config and self.config.encfs_enabled:
            return method(self, *method_args, **method_kwargs)

    return __wrapper


class CryptProvider(CommandRunner):
    """
    Provides encryption related methods.
    """
    binary_name: str = "encfs"
    accepted_version: tuple = (1, 9, 5)

    config: ConfigEntry = None
    """Config to be set manually with `set_config()` method."""

    __resource_mounted: bool = False
    """
    Mount flag to tell us if we have the resource mounted or not.
    This should be managed automatically by the functions.
    """

    def version_detect(self):
        # detect binary path
        which_result = self.os_exec(["which", self.binary_name], silent=True)
        self.binary_path = str(which_result.stdout).strip()

        # detect/parse the version
        version_check_result = self.os_exec([self.binary_path, "--version"], silent=True)
        result_string = str(version_check_result.stderr).strip()
        matched_string = re.search(r"^encfs\s+version\s+(\d.*\.\d)\s*$", result_string)
        if not matched_string:
            raise SystemExit(f"Error! Unmatched version string for: {self.binary_path}!\n{version_check_result}")
        version_string = matched_string.groups()[0]
        self.detected_version = tuple([
            int(num) for num in version_string.split('.')
        ])

    def cleanup(self):
        self.__unmount_encfs()

    @validate_config
    def __unmount_encfs(self):
        """
        Unmounts the data access directory.
        """
        print("Unmounting EncFS...")
        if not self.__resource_mounted:
            print("... skipped - already unmounted!")
            return

        which_result = self.os_exec(["which", "umount"], silent=True)
        umount_binary = str(which_result.stdout).strip()
        exec_command: list = [umount_binary, self.config.encfs_decryption_dir]

        umount_result = self.os_exec(exec_command, confirmation_required=True)
        self.__resource_mounted = False

        run_report = self.gen_run_report(exec_command, umount_result.stdout, umount_result.stderr)
        Logger.log(run_report)

    @validate_config
    def __mount_encfs(self):
        """
        Mounts the data access directory.
        """
        print("Mounting EncFS...")
        if self.__resource_mounted:
            print("... skipped - already mounted!")
            return

        exec_command: list = [self.binary_path, self.config.encfs_encryption_dir, self.config.encfs_decryption_dir]
        mount_result = self.os_exec(exec_command, confirmation_required=True, capture_output=False)
        self.__resource_mounted = True

        run_report = self.gen_run_report(exec_command, mount_result.stdout, mount_result.stderr)
        Logger.log(run_report)

    def set_config(self, config: ConfigEntry):
        """
        Set the config to work with.
        """
        self.config = config

    @validate_config
    def run(self, action: BackupAction):
        self.__mount_encfs()
