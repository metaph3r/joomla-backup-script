import logging
from pathlib import Path
import backup.backup_config as config
import backup.backup as backup
from backup.logging_config import configure_logging

CONFIG_FILE = "config.ini"

def get_backup_config_filepath() -> Path:
    current_dir = Path.cwd()
    config_file_path = current_dir / CONFIG_FILE
    return config_file_path

if __name__ == "__main__":
    try:
        backup_config = config.BackupConfig(get_backup_config_filepath())
        log_file_path = configure_logging(backup_config.backup_log)
        logger = logging.getLogger(__name__)
        joomla_backup = backup.JoomlaBackup(backup_config)
        joomla_backup.run_backup()
    except Exception as e:
        logger.exception("Error occurred: %s", e)
        exit(1)
