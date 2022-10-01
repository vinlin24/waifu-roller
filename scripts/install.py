"""install.py

Helper script for installing a fresh copy of the latest whl
distribution in my global environment.
"""

from pathlib import Path
import sys
import subprocess

CONFIG_FILE_PATH = Path.home() / ".config/waifu-roller/config.yaml"

_print = print


def print(*args, **kwargs) -> None:
    """Redefine print for minimal log-like outputs."""
    return _print(f"[{Path(__file__).name}]", *args, **kwargs)


def get_python_path() -> Path:
    """Return resolved path to the global interpreter, probably."""
    return (Path(sys.base_prefix) / "python.exe").resolve()


def get_latest_dist() -> Path | None:
    dist_path = Path(__file__).parent / "../dist"
    path = None
    # They should already be sorted by the x.y.z part of their names
    for path in dist_path.iterdir():
        pass
    if path is not None:
        path = path.resolve()
        print(f"Using distribution {path}.")
    else:
        print("Could not find a whl file to install.")
    return path


def install_dist_globally(whl: Path) -> None:
    python_path = get_python_path()
    cmd = f"{python_path} -m pip install {whl} --force-reinstall"
    subprocess.run(cmd, check=True)
    print(f"Installed {whl} with Python interpreter at {python_path}.")


def remove_config_file() -> None:
    try:
        CONFIG_FILE_PATH.unlink()
        print(f"Deleted config file at {CONFIG_FILE_PATH}.")
    except FileNotFoundError:
        print(
            f"Could not find config file at {CONFIG_FILE_PATH}, "
            "deleted nothing."
        )


def main() -> None:
    """Main driver function."""
    # Get the latest distribution, if it exists
    dist_path = get_latest_dist()
    if dist_path is None:
        sys.exit(1)

    # Install with global Python, probably
    install_dist_globally(dist_path)

    # If successful, remove user's existing config file for fresh start
    remove_config_file()

    # Tell user to verify that the package is installed
    print(
        "Verify that the package is installed globally by running 'waifu "
        "--version' outside of your virtual environment."
    )


if __name__ == "__main__":
    main()
