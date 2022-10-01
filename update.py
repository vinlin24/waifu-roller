"""update.py

Script to use the metadata.version value in setup.cfg to update
appropriate files as part of a pre-build checklist.
"""

import configparser
import re
from pathlib import Path


def AbsPath(relative: str) -> Path:
    """Helper function for working with paths.

    Args:
        relative (str): Relative path string. Paths should be relative
        to this file (i.e. "." refers to this file's directory).

    Raises:
        FileNotFoundError: The path does not exist.

    Returns:
        Path: Resolved absolute path instance.
    """
    path = Path(relative).resolve()
    # Raise this earlier than later
    if not path.exists():
        raise FileNotFoundError(path)
    return path


# Absolute paths
SETUP_CFG_PATH = AbsPath("./setup.cfg")
PACKAGE_INIT_PATH = AbsPath("./src/waifu/__init__.py")


def get_version() -> str:
    """Get the value of metadata.version in the setup.cfg file."""
    # Load cfg
    config = configparser.ConfigParser()
    config.read(SETUP_CFG_PATH)
    version = config["metadata"]["version"]
    print(
        f"[update.py] Successfully extracted string {version!r} "
        f"from {SETUP_CFG_PATH}."
    )
    return version


def update_init(version: str) -> None:
    """Update the value of __version__ in the source __init__.py."""
    updated_line = f"__version__ = \"{version}\""

    # Match the line that __version__ is assigned on
    version_finder = re.compile(r"^__version__ ?= ?.*$", re.MULTILINE)

    with PACKAGE_INIT_PATH.open("rt+", encoding="utf-8") as fp:
        content = fp.read()
        match = version_finder.search(content)

        # __version__ isn't assigned yet, append the line
        if match is None:
            # Changed 0.0.3: originally you would've overwritten at pos 0 :/
            fp.seek(0, 2)  # this means 0 byte offset from end of file
            fp.write(updated_line)
        # Otherwise replace that line
        else:
            start, end = match.start(), match.end()
            updated_content = content[:start] + updated_line + content[end:]
            fp.truncate(0)
            fp.seek(0)
            fp.write(updated_content)

    print(f"[update.py] INFO: Successfully updated {PACKAGE_INIT_PATH}")


def main() -> None:
    """Main driver function."""
    version = get_version()
    update_init(version)


if __name__ == "__main__":
    main()
