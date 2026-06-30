import logging
from pathlib import Path


def configure_logging(log_file_name: str) -> Path:
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)
        handler.close()

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    log_file_path = Path(__file__).resolve().parent.parent / log_file_name
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    return log_file_path
