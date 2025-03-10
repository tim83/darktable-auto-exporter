import argparse
import subprocess
from . import xmp_manager, exporter


def main():
    parser = argparse.ArgumentParser(
        description="Automatically export all (changed) images in a darktable library."
    )
    parser.add_argument(
        "action",
        type=str,
        help="The action to be taken",
        choices=["export", "list", "darktable_version"],
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force export of all images, even if they are unchanged.",
    )

    args = parser.parse_args()
    match args.action:
        case "export":
            exporter.export()
        case "list":
            list(xmp_manager.get_xmp_files())
        case "darktable_version":
            darktable_version()
        case _:
            raise ValueError(f"Unknown action: {args.action}")


def darktable_version():
    subprocess.run(["darktable-cli", "--version"])


if __name__ == "__main__":
    main()
