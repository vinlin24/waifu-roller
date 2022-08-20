"""
open.py
22 July 2022 23:54:06

Responsible for starting/opening the Discord desktop app/webpage.
"""

import os
import pathlib
import platform
import time

import pyautogui

from exceptions import DiscordNotFoundError, OSNotSupportedError

# make configurable later?
LOAD_WAITING = 5.0  # seconds to wait before continuing if starting app


def _get_exe_path() -> pathlib.Path:
    """Generate the path to the Discord executable.

    Raises:
        DiscordNotFoundError: Could not locate Discord.exe.

    Returns:
        pathlib.Path: The path to the Discord executable.
    """
    # (Windows) By default, Discord is installed at:
    # C:\Users\%username%\AppData\Local\Discord
    home_path = pathlib.Path.home()
    discord_path = home_path / "AppData/Local/Discord/"
    app_folder = None
    for filename in os.listdir(discord_path):
        if filename.startswith("app-"):
            app_folder = filename
            break
    else:
        raise DiscordNotFoundError("Could not located Discord.exe")

    exe_path = discord_path / app_folder / "Discord.exe"
    return exe_path


def _start_discord() -> None:
    """Start the Discord desktop application and wait for a delay."""
    exe_path = _get_exe_path()
    os.startfile(exe_path)
    time.sleep(LOAD_WAITING)


def _move_to_discord(win: pyautogui.Window) -> None:
    """Move to the Discord desktop application window."""
    win.maximize()
    win.activate()


# function to call in main process
def open_discord() -> None:
    """Open or move to the Discord desktop application.

    Raises:
        OSNotSupportedError: If the application is not running on Windows (WIP).
        DiscordNotFoundError: Could not locate Discord.exe.
    """
    # get windows working first, then worry about cross-platform lol
    if platform.system() != "Windows":
        raise OSNotSupportedError(
            "Application only supports Windows at the moment")

    # if _is_discord_running():
    #     _move_to_discord()
    # else:
    #     _start_discord()
