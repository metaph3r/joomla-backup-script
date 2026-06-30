# Joomla Backup Script

A Python utility to create local backups of a remote Joomla site and its MySQL database using SSH.

## What it does

- connects to a remote host via SSH
- archives the Joomla site files using `tar`
- dumps the Joomla MySQL database using `mysqldump`
- compresses the backups and stores them locally
- removes old `.gz` backups after the configured retention period

## Requirements

- Python 3
- `ssh` available locally
- remote `tar` available on the backup host
- remote `mysqldump` available on the backup host
- a configured `config.ini` file
- public SSH key must be installed on the backup host for passwordless SSH access
- remote MySQL credentials can be provided via a `.my.cnf` file for the database user

## Configuration

Copy `config.ini.template` to `config.ini` in the project root and update the example values with your site-specific settings.

The template includes meaningful placeholder values for each section:

- `General`
  - `backup_host`: SSH host to connect to
  - `backup_user`: SSH user to connect as
  - `backup_retention_days`: number of days to retain backups locally
  - `backup_path`: local directory where backup files are saved
- `Files`
  - `webspace_path`: remote POSIX base path for the Joomla installation
  - `joomla_path`: Joomla folder path under `webspace_path` on the remote host
  - `backup_filename_suffix`: file suffix for the Joomla backup archive
- `Database`
  - `host`: MySQL host
  - `name`: Joomla database name
  - `backup_filename_suffix`: file suffix for the database backup

The script generates timestamped backup files based on the current date and time.

## Usage

From the project root, run:

```bat
python main.py
```

If the executable has been built, you can also run it from the same directory where `config.ini` is located.

For example on Windows:

```bat
backup-joomla-site.exe
```

Or on Linux/WSL:

```bash
./backup-joomla-site
```

## Build the executable

### Windows

Run the batch script from the project root:

```bat
build_exe.bat
```

### Linux / WSL

Run the shell script from the project root:

```bash
chmod +x build_exe.sh
./build_exe.sh
```

After building, place `config.ini` in the same directory as the executable so the program can load its configuration.
