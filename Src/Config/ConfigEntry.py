import json

from Src.Config.ConfigVersion import ConfigVersion


class ConfigEntry:
    """
    Config entry entity.
    """

    def __init__(self):
        """
        Initializes the entry.
        """
        self.config_version: float = ConfigVersion.config_version
        self.general_name: str = ''
        self.backup_source_dir: str = ''
        self.backup_target_dir: str = ''
        self.encfs_enabled: bool = False
        self.encfs_encryption_dir: str = ''
        self.encfs_decryption_dir: str = ''

    def to_json(self) -> str:
        """
        Converts the entry to the json string.
        """
        json_string = json.dumps(vars(self),
                                 sort_keys=True,
                                 indent=4)
        return json_string

    def from_json(self, json_string: str) -> bool:
        """
        Fills up the entry with data from json.
        """
        def read_json_field(field_name: str, optional: bool = False):
            """
            Parses single json field.
            """
            try:
                return parsed_json[field_name]
            except (KeyError, AttributeError):
                if not optional:
                    print("Failed to import the configuration! Failed on parsing field: " + field_name)
                    raise KeyError("Failed to parse json!")

        parsed_json = json.loads(json_string)

        # required fields
        try:
            self.config_version = read_json_field('config_version')
            if self.config_version != ConfigVersion.config_version:
                raise SystemExit("Wrong config version!")

            self.general_name = read_json_field('general_name')
            self.backup_source_dir = read_json_field('backup_source_dir')
            self.backup_target_dir = read_json_field('backup_target_dir')
            self.encfs_enabled = read_json_field('encfs_enabled')

            # optional fields
            self.encfs_encryption_dir = read_json_field('encfs_encryption_dir', True)
            self.encfs_decryption_dir = read_json_field('encfs_decryption_dir', True)
        except KeyError:
            return False

        return True

    def string_summarize(self) -> str:
        """
        Returns a short summary in string format.
        """
        def summarize_line(line: str, value: str) -> str:
            return str(f"\n{line}: \n >> {value}")

        summary = ''.join([
            summarize_line("General name", self.general_name),
            summarize_line("Backup source", self.backup_source_dir),
            summarize_line("Backup target", self.backup_target_dir),
            summarize_line("EncFS: Encryption enabled", str(self.encfs_enabled))
        ])

        if self.encfs_enabled:
            summary += ''.join([
                summarize_line("EncFS: Encrypted (store) data directory", self.encfs_encryption_dir),
                summarize_line("EncFS: Decrypted (access) data directory", self.encfs_decryption_dir)
            ])

        return summary
