#!/usr/bin/env python3

from Src.Common.BackupAction import BackupAction
from Src.Config.ConfigEntry import ConfigEntry
from Src.Config.ConfigManager import ConfigManager
from Src.IO.UserInputConsole import UserInputConsole
from Src.Service.CryptProvider import CryptProvider
from Src.Service.SyncProvider import SyncProvider


class EESync:
    __version = '0.2'

    sync_service = SyncProvider()
    crypt_service = CryptProvider()

    def start(self):
        """
        Starts the main process.
        """
        print(f"~~ EESync {self.__version} ~~")
        self.sync_service.version_check()
        self.crypt_service.version_check()
        print()

        self.interactive_user_menu()
        print("Finished")

    def interactive_user_menu(self):
        """
        Handles the interactive user menu - main menu.
        """
        cm_object = ConfigManager()
        cm_object.search_config_entries()

        if len(cm_object.config_list):
            entry_list_string = ''
            for config_entry in cm_object.config_list:
                entry_list_string += str(
                    f"  {config_entry['config_number']} - {config_entry['general_name']}\n"
                )

            print("Found saved config entries. \n"
                  + entry_list_string
                  + "Please choose the number to load, or type 'n' to create a new entry.")
            user_input = UserInputConsole.read_config_no()
        else:
            print("No saved config entries found.")
            user_input = 'n'

        match user_input:
            case number if user_input.isdigit():
                print("Selected entry no. " + number + " ...")
                selected_config = cm_object.config_list[int(number) - 1]
                self.process_entry(selected_config['config_object'])
                pass
            case 'n':
                print("Creating new config.")
                new_config_entry = cm_object.new_entry_from_user()
                cm_object.save_config_entry(new_config_entry)
                self.interactive_user_menu()
            case _:
                print("Wrong command!")
                raise SystemExit("Not supported mode!")

    def process_entry(self, entry: ConfigEntry):
        """
        Handles the interactive user menu - selected entry menu.
        """

        # ask the user for the action
        action_list = ''
        for action in BackupAction:
            action_description = BackupAction.describe_action(action)
            action_list += str(f"\n  {action.value} - {action.name} - {action_description}")
        print(f"Successfully loaded: {entry.general_name}\n"
              + "Please select the action: "
              + action_list)
        user_action = UserInputConsole.read_action()

        # ask for the final review and confirmation
        print(
            f"\nYou are bout to run the action: {user_action.name} \n"
            + "for following configuration: \n"
            + f" Data directory: \n >> {entry.backup_source_dir}\n"
            + f" Backup data directory: \n >> {entry.backup_target_dir}\n"
            + f" Encryption enabled: \n >> {entry.encfs_enabled}"
        )
        if entry.encfs_enabled:
            print(f" Decrypted backup data directory: \n >> {entry.encfs_decryption_dir}")
        print("Is this correct?")
        final_acceptance = UserInputConsole.read_true_or_false()

        # proceed with final action
        if final_acceptance:
            self.sync_service.set_config(entry)
            if entry.encfs_enabled:
                self.crypt_service.set_config(entry)
                self.crypt_service.run(user_action)
            self.sync_service.run(user_action)
        else:
            print("Aborted.")
