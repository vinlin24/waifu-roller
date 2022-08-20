"""
open.py
22 July 2022 23:54:06

Responsible for starting/opening the Discord desktop application.
"""

import os
import pathlib
import platform

import pyautogui
import rich

from exceptions import (DiscordNotFoundError, DiscordNotOpenError,
                        OSNotSupportedError)


def _get_exe_path() -> pathlib.Path:
    """Generate the path to the Discord launcher executable.

    Raises:
        DiscordNotFoundError: Could not locate the launcher executable.

    Returns:
        pathlib.Path: The path to the Discord executable.
    """
    system_name = platform.system()
    # (Windows) By default, the path to the Discord launcher is:
    # C:\Users\%username%\AppData\Local\Discord\Update.exe
    # equivalently: %LocalAppdata%\Discord\Update.exe
    # Note: this is different from the actual client executable,
    # which is at %LocalAppdata%/Discord/app-[version]/Discord.exe
    # https://www.reddit.com/r/discordapp/comments/mfug1g/where_is_the_exact_location_for_discordexe/
    if system_name == "Windows":
        home_path = pathlib.Path.home()
        discord_path = home_path / "AppData/Local/Discord/"
        for filename in os.listdir(discord_path):
            if filename.startswith("app-"):
                return discord_path / filename / "Discord.exe"
    # Get windows working first, then worry about cross-platform lol
    else:
        raise OSNotSupportedError(
            "Application does not recognize or support system/OS "
            f"{system_name!r} at the moment"
        )

    raise DiscordNotFoundError(
        "Could not locate launcher executable "
        f"(Platform: {system_name})"
    )


def _start_discord() -> None:
    """Start the Discord desktop application."""
    exe_path = _get_exe_path()
    rich.print("[bright_black]Starting Discord executable...[/]")
    os.startfile(exe_path)
    rich.print("[bright_black]Launched Discord desktop application[/]")


def _move_to_discord() -> None:
    """Move to the Discord desktop application window."""
    # filter list to find the one that's most likely the desktop app
    win_list: list[pyautogui.Window] = \
        pyautogui.getWindowsWithTitle("Discord")
    for win in win_list:
        title: str = win.title
        if title == "Discord" or title.endswith("- Discord"):
            break
    else:
        raise DiscordNotOpenError(
            "Could not find a window resembling the Discord desktop "
            "application out of the windows with 'Discord' in the title: "
            f"{win_list or '<empty>'}"
        )
    win.maximize()
    win.activate()
    rich.print("[bright_black]Moved to the Discord desktop application[/]")


def open_discord() -> bool:
    """Open or move to the Discord desktop application.

    Interface function to be called from main process.

    Raises:
        OSNotSupportedError: If the application is not running on
        Windows (work-in-progress).
        DiscordNotFoundError: Could not locate Discord.exe.

    Returns:
        bool: Whether the application had to be manually started.
    """
    try:
        _move_to_discord()
        return False
    except DiscordNotOpenError:
        rich.print(
            "[yellow]Could not detect Discord desktop application among "
            "currently open windows[/]"
        )
        _start_discord()
        return True
    # The return bool can then be used in the main process to decide if
    # it should immediately start the keystroke sequence or wait for the
    # the user to hit <ENTER> first. I think this is a better system than
    # my original idea of waiting for an arbitrary timeout to assume the
    # Discord app is finished loading.
