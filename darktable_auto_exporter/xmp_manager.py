import hashlib
import typing

from . import settings
from pathlib import Path


def get_xmp_files() -> typing.Generator[Path, None, None]:
    if not settings.RAW_DIRECTORY.is_dir():
        raise NotADirectoryError(f"{settings.RAW_DIRECTORY=} is not a directory.")
    xmp_file: Path
    for xmp_file in settings.RAW_DIRECTORY.rglob("*.xmp"):
        if ".Trash-1000" not in str(xmp_file.parent):
            yield xmp_file


def hash_xmp_file(xmp_file: Path) -> str:
    return hashlib.sha256(xmp_file.read_bytes()).hexdigest()


def ensure_export_log_exists() -> None:
    if not settings.EXPORT_LOG_FILE.exists():
        with settings.EXPORT_LOG_FILE.open(mode="w") as f:
            f.write("SIDE_CAR_FILE,MODIFICATION_TIME,SHA256,EXPORT_FILE\n")


def record_export(xmp_file: Path, export_file: Path) -> None:
    with settings.EXPORT_LOG_FILE.open("a") as f:
        f.write(
            f"{xmp_file},{xmp_file.lstat().st_mtime},{hash_xmp_file(xmp_file)},{export_file}\n"
        )


def has_xmp_changed(xmp_file: Path) -> bool:
    with settings.EXPORT_LOG_FILE.open("r") as f:
        for line in f:
            if line.startswith(f"{xmp_file},"):
                cols = line.split(",")
                match settings.CHANGE_DETECTION_METHOD:
                    case settings.ChangeDetectionMethods.SHA256:
                        return hash_xmp_file(xmp_file) != cols[2]
                    case settings.ChangeDetectionMethods.MODIFICATION_TIME:
                        return xmp_file.lstat().st_mtime != cols[1]
                    case _:
                        raise ValueError(
                            f"Unknown change detection method: {settings.CHANGE_DETECTION_METHOD}"
                        )
    return True


def get_image_file(xmp_file: Path) -> Path:
    return xmp_file.with_suffix("")
