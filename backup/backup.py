import shlex
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
            print(f"{type.value.capitalize()} backup completed successfully as {path / file} in {end_time - start_time:.2f} seconds.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error during backup: {e.stderr.decode()}")

    def _backup_files(self):
        remote_webspace_path = shlex.quote(str(self._config.webspace_path))
        remote_joomla_path = shlex.quote(str(self._config.joomla_path))
        self._execute_backup(
            file=self._config.joomla_backup_filename,
            command=f"tar -czf - -C {remote_webspace_path} {remote_joomla_path}",
            type=BackupType.FILES
        )

    def _backup_database(self):
        db_host = shlex.quote(self._config.db_host)
        db_name = shlex.quote(self._config.db_name)
        self._execute_backup(
            file=self._config.db_backup_filename,
            command=f"mysqldump --single-transaction --no-tablespaces -h {db_host} {db_name} | gzip -c",
            type=BackupType.DATABASE
        )

    def _cleanup(self):
        retention_seconds = self._config.backup_retention_days * 24 * 60 * 60
        cutoff = time.time() - retention_seconds
        backup_path = self._config.backup_path
        count = 0
        print(f"Cleaning up old backups in {backup_path} older than {self._config.backup_retention_days} days...")

        for file in backup_path.iterdir():
            if file.is_file() and file.suffix == ".gz":
                try:
                    if file.stat().st_mtime < cutoff:
                        file.unlink()
                        print(f"Deleted old backup: {file}")
                        count += 1
                except Exception as e:
                    raise RuntimeError(f"Failed to delete backup {file}: {e}")

        print(f"Cleanup completed. Deleted {count} old backups.")

    def run_backup(self):
        if not self._config.backup_path.exists() or not self._config.backup_path.is_dir():
            print(f"Backup path does not exist or is not a directory: {self._config.backup_path}")
            return

        print(f"Starting backup process for Joomla site at {(self._config.webspace_path / self._config.joomla_path).as_posix()} and database {self._config.db_name}...")
        self._backup_database()
        self._backup_files()
        self._cleanup()
        print("Backup process completed successfully.")
