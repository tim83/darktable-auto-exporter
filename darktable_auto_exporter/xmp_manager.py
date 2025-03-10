import hashlib
import typing
import xml.etree.ElementTree as ET
from . import settings
from pathlib import Path


def get_xmp_files() -> typing.Generator[Path, None, None]:
    if not settings.RAW_DIRECTORY.is_dir():
        raise NotADirectoryError(f"{settings.RAW_DIRECTORY=} is not a directory.")
    xmp_file: Path
    for xmp_file in settings.RAW_DIRECTORY.rglob("*.xmp"):
        if ".Trash-1000" not in str(xmp_file.parent):
            yield xmp_file

def read_xmp_file(xmp_file: Path) -> ET.Element:
    return ET.parse(xmp_file).getroot()

def hash_xmp_file(xmp_file: Path) -> str:
    return hashlib.sha256(xmp_file.read_bytes()).hexdigest()


def record_export(xmp_file: Path, export_file: Path) -> None:
    if not settings.EXPORT_LOG_FILE.exists():
        with settings.EXPORT_LOG_FILE.open(mode="w") as f:
            f.write("SIDE_CAR_FILE,MODIFICATION_TIME,SHA256,EXPORT_FILE,SELECTED\n")

    with settings.EXPORT_LOG_FILE.open("a") as f:
        f.write(
            f"{xmp_file},{xmp_file.lstat().st_mtime},{hash_xmp_file(xmp_file)},{export_file},True\n"
        )

def record_discard(xmp_file: Path) -> None:
    if not settings.EXPORT_LOG_FILE.exists():
        return
    with settings.EXPORT_LOG_FILE.open("a") as f:
        f.write(
            f"{xmp_file},{xmp_file.lstat().st_mtime},{hash_xmp_file(xmp_file)},,False\n"
        )


def has_xmp_changed(xmp_file: Path) -> bool:
    if not settings.EXPORT_LOG_FILE.exists():
        return True
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

def has_been_selected(xmp_file: Path) -> bool:
    print(read_xmp_file(xmp_file)[0],read_xmp_file(xmp_file)[0][0], read_xmp_file(xmp_file)[0][0].attrib)
    return read_xmp_file(xmp_file)[0][0].attrib["{http://ns.adobe.com/xap/1.0/}:Rating"] != "-1"

def get_image_file(xmp_file: Path) -> Path:
    return xmp_file.parent / read_xmp_file(xmp_file)[0][0].attrib['{http://ns.adobe.com/xap/1.0/mm/}DerivedFrom']
