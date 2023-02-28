import os
import re
from datetime import datetime

from Src.Config.ConfigEntry import ConfigEntry
from Src.Config.ConfigVersion import ConfigVersion
from Src.IO.UserInputConsole import UserInputConsole


class ConfigManager:
    """
    Config files provider.
    """

    config_directory: str
    """config files location."""

    config_list: list
    """matched configs - file names."""

    selected_entry: ConfigEntry
    """current entry to work with."""

    def __init__(self):
        """
        Initialize the class.
        """
        self.config_list = []
        self.config_match_regex = re.compile(".*[.]" + ConfigVersion.config_files_extension + "$")
        self.config_directory = self.get_config_directory()

        if not os.path.isdir(self.config_directory):
            raise SystemExit("Wrong config directory! Not a directory: " + self.config_directory)

    @classmethod
    def get_config_directory(cls):
        """
        Returns the config directory. Can be called before the object is created.
        :return: str: config directory path.
        """
        return ConfigVersion.config_files_directory

    def search_config_entries(self):
        """
        Search for the saved configurations.
        """
        config_number = 0
        for file_name in sorted(os.listdir(self.config_directory)):
            if self.config_match_regex.match(file_name):
                config_number += 1

                file_path = self.config_directory + '/' + file_name

                with open(file_path, 'r') as file:
                    file_content_lines = file.readlines()
                    file_content = ''.join(file_content_lines)

                loaded_entry = ConfigEntry()
                if not loaded_entry.from_json(file_content):
                    raise SystemExit('Failed to load data from config! Failed on file: ' + file_path)

                self.config_list.append({
                    "config_number": config_number,
                    "file_name": file_name,
                    "file_path": file_path,
                    "file_content": file_content,
                    "general_name": loaded_entry.general_name,
                    "config_object": loaded_entry
                })

    def save_config_entry(self, entry: ConfigEntry):
        """
        Saves the ConfigEntry.
        """
        # remove non-ASCII characters and spaces from the name
        filtered_name = ''
        for character in entry.general_name:
            if ord(character) < 128 and character != ' ':
                filtered_name += character

        save_file_name = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                             + '_' + filtered_name
                             + '.' + ConfigVersion.config_files_extension
                             )[:255]

        # prepare the location
        save_path = str(self.config_directory + '/' + save_file_name)

        if os.path.isfile(save_path):
            raise SystemExit("File exists! Cannot save to: " + save_path)

        # save the file
        with open(save_path, 'w') as file:
            file.write(entry.to_json())

    @staticmethod
    def new_entry_from_user() -> ConfigEntry:
        """
        Prepare new config entry - interactive mode.
        """
        new_entry = ConfigEntry()

        print("Please provide a general (user friendly) name for the backup. ")
        new_entry.general_name = UserInputConsole.general_input()

        print("Please provide source directory (location to be backed up, e.g. your local folder). ")
        new_entry.backup_source_dir = UserInputConsole.read_directory_path()
        print("Please provide target directory (backup save location, e.g. external or network drive). ")
        new_entry.backup_target_dir = UserInputConsole.read_directory_path()

        print("Would you like to enable the encfs encryption for the storage? [y/n] ")
        if UserInputConsole.read_true_or_false():
            new_entry.encfs_encryption_dir = new_entry.backup_target_dir
            print("Please provide decryption directory. \n"
                  + "This location will be used as a mount-place for accessing your encrypted data. \n"
                  + "Please note that this is not the place to store the backup data. \n"
                  + "This is the place to access the encrypted backup. \n"
                  + "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n"
                  + "!PLEASE NOTE that this should be placed outside the locations that you provided before!")
            new_entry.encfs_decryption_dir = UserInputConsole.read_directory_path()
            new_entry.encfs_enabled = True
        else:
            new_entry.encfs_enabled = False

        print("\nPlease review: \n" + new_entry.string_summarize()
              + "\n\nIs above correct?")
        if not UserInputConsole.read_true_or_false():
            return ConfigManager.new_entry_from_user()

        return new_entry
