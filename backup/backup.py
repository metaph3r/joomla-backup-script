import subprocess
import time
from pathlib import Path

from backup.backup_config import BackupConfig
from backup.backup_type import BackupType

class JoomlaBackup:
    def __init__(self, config: BackupConfig):
        self._config = config

    def _execute_backup(self, file: Path, command: str, type: BackupType):
        host = self._config.backup_host
        user = self._config.backup_user
        path = self._config.backup_path
        print(f"Backing up {type.value} as {path / file}...")
        try:
            start_time = time.perf_counter()
            result = subprocess.run(
                [
                    "ssh",
                    f"{user}@{host}",
                    command
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            with open(path / file, "wb") as f:
                f.write(result.stdout)
            end_time = time.perf_counter()
            print(f"{type.value.capitalize()} backup completed successfully as {path / file} in {end_time - start_time:.2f} seconds")
        except subprocess.CalledProcessError as e:
            print(f"Error during backup: {e.stderr.decode()}")

    def _backup_files(self):
        self._execute_backup(
            file=self._config.joomla_backup_filename,
            command=f"tar -czf - -C {self._config.webspace_path.as_posix()} {self._config.joomla_path.as_posix()}",
            type=BackupType.FILES
        )

    def _backup_database(self):
        self._execute_backup(
            file=self._config.db_backup_filename,
            command=f"mysqldump --single-transaction --no-tablespaces -h {self._config.db_host} {self._config.db_name} | gzip -c",
            type=BackupType.DATABASE
        )

    def run_backup(self):
        self._backup_database()
        self._backup_files()
