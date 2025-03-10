import enum

import dotenv
import os
from pathlib import Path

dotenv.load_dotenv()
RAW_DIRECTORY: Path = Path(os.getenv("RAW_DIRECTORY"))
OUT_DIRECTORY: Path = Path(os.getenv("OUT_DIRECTORY"))
OUT_FORMAT: str = os.getenv("OUT_FORMAT", ".jpg")

EXPORT_LOG_FILE: Path = Path(
    os.getenv("EXPORT_LOG", OUT_DIRECTORY / ".darktable-auto-exporter.log")
)


class ChangeDetectionMethods(enum.Enum):
    MODIFICATION_TIME = enum.auto()
    SHA256 = enum.auto()


CHANGE_DETECTION_METHOD: ChangeDetectionMethods = os.getenv(
    "CHANGE_DETECTION_METHOD", ChangeDetectionMethods.SHA256
)
