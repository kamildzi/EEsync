#!/usr/bin/env python3

import os
import re

from Src.Common.BackupAction import BackupAction
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

    def run(self, action: BackupAction):

        # require config to be set before the run() is fired
        if not self.config:
            raise SystemExit(f"Internal Error! Action: {action} requested before config is set!")

        # encrypted entries support
        if self.config.encfs_enabled:
            effective_target_dir = str(self.config.encfs_decryption_dir + '/')
        else:
            effective_target_dir = str(self.config.backup_target_dir + '/')

        effective_source_dir = str(self.config.backup_source_dir + '/')

        # action mapping
        match action:
            case BackupAction.BACKUP:
                self.__exec_rsync(effective_source_dir, effective_target_dir, False)
            case BackupAction.BACKUP_DRY:
                self.__exec_rsync(effective_source_dir, effective_target_dir, True)
            case BackupAction.RESTORE:
                self.__exec_rsync(effective_target_dir, effective_source_dir, False)
            case BackupAction.RESTORE_DRY:
                self.__exec_rsync(effective_target_dir, effective_source_dir, True)
            case _:
                raise SystemExit("Error! Wrong action: " + action.name)

    def __exec_rsync(self, source_dir: str, target_dir: str, dry_run: bool):
        """
        Executes the rsync command.
        :param source_dir: Source directory - what to copy?
        :param target_dir: Target directory - where to save a copy?
        :param dry_run: Should we do a test run? True means that rsync will only list the changes (but will not do anything to the files)
        """

        # validate source and target directories
        for path in (source_dir, target_dir):
            if not os.path.isdir(path):
                raise SystemExit("Error! Not a directory: " + path)

        # prepare the command
        rsync_base_params: list = [
            "-avh", "--delete"
        ]
        if dry_run:
            rsync_base_params += ["--dry-run"]

        exec_command: list = [self.binary_path] + rsync_base_params + [source_dir, target_dir]

        # run the command
        rsync_result = self.os_exec(exec_command, True)

        # save the report
        # TODO - save it to a file
        run_report = str("--- STDOUT: ---\n"
                         + rsync_result.stdout
                         + "--- STDERR: ---\n"
                         + rsync_result.stderr)
        print(run_report)

        print("Done!")
