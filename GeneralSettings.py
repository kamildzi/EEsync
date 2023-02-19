# General settings. Adjust these to your needs.

runner = {

    # Prints the external (backup) commands that are executed on your OS.
    # Asks for confirmation before running the command.
    # Possible values: "True" or "False".
    "confirm_os_commands": True
}

logger = {

    # Choose the logging method.
    # Available methods - uncomment one:
    "log_method": "stdout",  # Standard output (console output).
    # "log_method": "file",  # Logs to a file.
    # "log_method": "none",  # No logs at all.

    # If "log_method" is set to a "File", then this setting can be used to define custom log directory.
    # Blank value ("") means that logs will be saved in application directory ("./SavedLogs").
    "custom_log_dir_path": ""
}
