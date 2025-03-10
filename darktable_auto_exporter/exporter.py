import subprocess
from pathlib import Path
from . import settings, xmp_manager


def get_export_file(xmp_file: Path) -> Path:
    return settings.OUT_DIRECTORY / xmp_file.relative_to(
        settings.RAW_DIRECTORY
    ).with_suffix("").with_suffix(settings.OUT_FORMAT)


def export(*, force: bool = False) -> None:
    for xmp_file in xmp_manager.get_xmp_files():
        export_file = get_export_file(xmp_file)
        if force or xmp_manager.has_xmp_changed(xmp_file):
            xmp_manager.record_export(xmp_file, export_file)
            print(f"Exporting {xmp_file} to {export_file}")
            subprocess.run(
                [
                    "darktable-cli",
                    str(xmp_manager.get_image_file(xmp_file)),
                    str(xmp_file),
                    str(export_file),
                ]
            )
        else:
            print(f"Skipping {xmp_file}, no changes detected.")
