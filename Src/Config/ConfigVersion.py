from os import getcwd


class ConfigVersion:
    """
    Common config settings.
    """

    config_version: float = 1.0
    """Config files format version."""

    config_files_extension: str = "conf"
    """File extension that configs are required to use."""

    config_files_directory: str = getcwd() + "/SavedConfig"
    """Directory that will be used for saving the configuration files."""
