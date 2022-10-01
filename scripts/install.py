"""install.py

Helper script for installing a fresh copy of the latest whl
distribution in my global environment.
"""

from pathlib import Path
import os
import sys
import subprocess

CONFIG_FILE_PATH = Path.home() / ".config/waifu-roller/config.yaml"


# Redefine print for minimal log-like outputs
_print = print


def print(*args, **kwargs) -> None:
    return _print(f"[{__file__}]", *args, **kwargs)


def get_latest_dist() -> Path | None:
    dist_path = Path(__file__).parent / "../dist"
    path = None
    # They should already be sorted by the x.y.z part of their names
    for path in dist_path.iterdir():
        pass
    if path is not None:
        print(f"Using distribution {path}.")
    else:
        print("Could not find a whl file to install.")
    return path


def install_dist(whl: Path) -> None:
    pip_cmd = "pip3" if os.name == "posix" else "pip"
    subprocess.run(f"{pip_cmd} install {whl}", check=True)
    print(f"Installed {whl}.")


def remove_config_file() -> None:
    try:
        CONFIG_FILE_PATH.unlink()
        print(f"Delete config file at {CONFIG_FILE_PATH}.")
    except FileNotFoundError:
        print(
            f"Could not find config file at {CONFIG_FILE_PATH}, "
            "deleted nothing."
        )


def main() -> None:
    """Main driver function."""
    # Install the latest distribution, if it exists
    dist_path = get_latest_dist()
    if dist_path is None:
        sys.exit(1)
    install_dist(dist_path)

    # If successful, remove user's existing config file for fresh start
    remove_config_file()

    # Verify that the package is installed
    print("Verifying installation by running: waifu --version")
    subprocess.run("waifu --version", check=True)


if __name__ == "__main__":
    main()
