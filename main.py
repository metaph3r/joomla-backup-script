import pathlib
import backup.backup_config as config
import backup.backup as backup

CONFIG_FILE = "config.ini"

def get_backup_config_filepath() -> str:
    current_dir = pathlib.Path.cwd()
    config_file_path = current_dir / CONFIG_FILE
    return str(config_file_path)

if __name__ == "__main__":
    backup_config = config.BackupConfig(get_backup_config_filepath()) 
    joomla_backup = backup.JoomlaBackup(backup_config)
    joomla_backup.run_backup()
