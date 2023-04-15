# General settings. Adjust these to your needs.

runner = {
    # Command runner (OS Exec) settings.

    # Prints the external (backup) commands that are executed on your OS.
    # Asks for confirmation before running the command.
    # Possible values: "True" or "False".
    "confirm_os_commands": True
}

logger = {
    # Logger settings.

    # Choose the logging method.
    # Available methods - uncomment one:
    # "log_method": "stdout_file",  # Use stdout and file methods - both at once.
    # "log_method": "stdout",  # Standard output (console output).
    "log_method": "file",  # Logs to a file.
    # "log_method": "none",  # No logs at all.

    # If "log_method" is set to a "File", then this setting can be used to define custom log directory.
    # Blank value ("") means that logs will be saved in application directory ("./SavedLogs").
    "custom_log_dir_path": "",

    # Allows to define number of days after which the logs will be deleted.
    # Empty value "" means than the feature is disabled (EEsync will not delete any logs on its own).
    # Note: for advanced logging control it is recommended to use a dedicated tool (like logrotate).
    "remove_logs_older_than_days": "14"
}

sync_rsync = {
    # Rsync settings and parameters.
    # Please make sure that you know what you're doing.
    # Options below will affect the file-synchronization process.
    # It is recommended for you to check following before you change anything in this section:
    # - rsync man pages: `https://linux.die.net/man/1/rsync`, `https://linux.die.net/man/5/rsyncd.conf`
    # - SyncProvider module in this project: `Src/Service/SyncProvider.py`

    # Base parameters that are provided for the rsync.
    "rsync_base_params": [
        "-ah", "--delete"
    ],

    # ----

    # Rsync has a nice logging feature ('--log-file' parameter).
    # Here, you can decide if you would like to use it or not.
    # Possible values: "True" or "False".
    # NOTE: Value if this setting a will also enable (or disable) other logging settings ("rsync_logging_*").
    "rsync_logging_enabled": True,

    # Below you may define extra parameters for the logging feature.
    "rsync_logging_extra_params": [
        "--log-file-format=\"[%t] [%p] %o %m %f %l\""
    ],

    # ----

    # Parameters that are added only if dry run mode is selected.
    "rsync_dry_run_params": [
        "--dry-run"
    ]
}
