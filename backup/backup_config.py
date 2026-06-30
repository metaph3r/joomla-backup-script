import configparser
import datetime
from pathlib import Path, PurePosixPath

def get_datetime_string() -> str:
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S")

class BackupConfig:
    backup_host: str
    backup_user: str
    backup_retention_days: int
    backup_path: Path
    backup_log: str
    webspace_path: Path
    joomla_path: Path
    joomla_backup_filename: str
    db_host: str
    db_name: str
    db_backup_filename: str

    def __init__(self, config_file: Path):
        if not config_file.exists():
            raise FileNotFoundError(f"Config file {config_file} does not exist.")

        config = configparser.ConfigParser()
        try:
            config.read(config_file)
        except Exception as e:
            raise RuntimeError(f"Error reading config file: {e}")

        self.backup_host = config.get("General", "backup_host")
        self.backup_user = config.get("General", "backup_user")
        self.backup_retention_days = config.getint("General", "backup_retention_days")
        self.backup_path = Path(config.get("General", "backup_path")).expanduser()
        self.backup_log = config.get("General", "backup_log")
        self.webspace_path = PurePosixPath(config.get("Files", "webspace_path"))
        self.joomla_path = PurePosixPath(config.get("Files", "joomla_path"))
        self.joomla_backup_filename = f"{get_datetime_string()}_{config.get('Files', 'backup_filename_suffix')}"
        self.db_host = config.get("Database", "host")
        self.db_name = config.get("Database", "name")
        self.db_backup_filename = f"{get_datetime_string()}_{config.get('Database', 'backup_filename_suffix')}"
