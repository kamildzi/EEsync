#!/usr/bin/env python3

import os
import re
from datetime import datetime

import GeneralSettings
from Src.Common.BackupAction import BackupAction
from Src.Config.ConfigEntry import ConfigEntry
from Src.IO.Logger import Logger
from Src.Service.CommandRunner import CommandRunner


class SyncProvider(CommandRunner):
    """
    Provides file-sync related methods.
    """
    binary_name: str = "rsync"
    accepted_version: tuple = (3, 2, 7)

    config: ConfigEntry = None
    """Config to be set manually with `set_config()` method."""

    def version_detect(self):
        # detect binary path
        which_result = self.os_exec(["which", self.binary_name], silent=True)
        self.binary_path = str(which_result.stdout).strip()

        # detect/parse the version
        version_check_result = self.os_exec([self.binary_path, "--version"], silent=True)
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
        rsync_settings = GeneralSettings.sync_rsync
        rsync_base_params: list = rsync_settings['rsync_base_params']

        if dry_run:
            rsync_base_params += rsync_settings["rsync_dry_run_params"]

        if rsync_settings["rsync_logging_enabled"]:
            # rsync logging - prepare the path
            current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_dir = Logger.get_log_path()
            rsync_log_path = log_dir + f"/rsync_{current_date}.log"
            if not os.path.isdir(log_dir) or os.path.isfile(rsync_log_path):
                raise SystemExit('Error! Rsync logging paths misconfigured!')

            # rsync logging - log to a file
            rsync_base_params += [f"--log-file={rsync_log_path}"]

            # rsync logging - extra params
            rsync_base_params += rsync_settings["rsync_logging_extra_params"]

        exec_command: list = [self.binary_path] + rsync_base_params + [source_dir, target_dir]

        # run the command
        rsync_result = self.os_exec(exec_command, confirmation_required=True, capture_output=False)

        # save the report
        run_report = self.gen_run_report(exec_command, rsync_result.stdout, rsync_result.stderr)
        Logger.log(run_report)

        print("Sync done!")
