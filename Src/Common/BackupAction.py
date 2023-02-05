from enum import Enum, unique


@unique
class BackupAction(Enum):
    BACKUP = 1
    BACKUP_DRY = 2
    RESTORE = 3
    RESTORE_DRY = 4

    @classmethod
    def describe_action(cls, action: "BackupAction"):
        match action.value:
            case cls.BACKUP.value:
                return "Regular backup"
            case cls.BACKUP_DRY.value:
                return "Dry run backup (only list the files)"
            case cls.RESTORE.value:
                return "Restore from the backup"
            case cls.RESTORE_DRY.value:
                return "Restore from the backup - dry run mode (only list the files)"
            case _:
                raise Exception(f"Undefined value for unmatched action: {action.name}!")
