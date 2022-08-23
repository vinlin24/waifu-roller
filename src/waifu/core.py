"""
core.py
20 August 2022 13:13:59

The bulk of the pyautogui calls.
"""

import threading
import time

import keyboard
import pyautogui
import rich

from waifu.exceptions import DiscordNotOpenError

# todo: Make configurable later
# The sleep calls are to prevent potential latency problems
# and to not appear suspicious.
ACTION_COOLDOWN = 0.1  # seconds to wait between actions
# TYPING_COOLDOWN = 0.05  # seconds to wait between character input
ROLLING_COOLDOWN = 1.0  # seconds to wait between waifu roll attempts

PAUSE_KEY = "capslock"

# Global flag for if autogui process is paused or not
paused = False


def _wait(delay: float) -> None:
    """Wait for at least delay seconds, and after paused flag if False.

    Args:
        delay (float): Minimum time in seconds to wait.
    """
    time.sleep(delay)
    # Block until unpaused
    while paused:
        pass


def _open_discord(verbose: bool) -> None:
    """Move to the Discord desktop application.

    Interface function to be called from main process.

    Args:
        verbose (bool): Configuration preference.

    Raises:
        DiscordNotOpenError: Could not locate the Discord desktop
        application as an open window.
    """
    # Filter list to find the one that's most likely the desktop app
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
    # minimize -> maximize trick is a workaround to the PyGetWinException
    # problem that happens when I try to accept input before activate()ing a
    # window: https://github.com/asweigart/PyGetWindow/issues/36#issuecomment-919332733
    win.minimize()
    win.maximize()
    win.activate()
    if verbose:
        rich.print("[bright_black]Moved to the Discord desktop application[/]")


def _navigate_to_channel(channel: str, verbose: bool) -> None:
    """Navigate to the target channel within Discord to roll in.

    This function does not guarantee that focus is brought to the
    desired channel is the argument is ill-defined.

    Args:
        channel (str): The command line argument that specifies the
        query string to submit to the Discord search bar to locate the
        channel to roll in.
        verbose (bool): Configuration preference.
    """
    # In case user put the # in there themselves
    search = "#" + channel.removeprefix("#")
    if verbose:
        rich.print(
            "[bright_black]Navigating by searching for channel with query "
            f"{search!r}...[/]"
        )

    # In case search bar was already up for some reason
    pyautogui.hotkey("esc")
    _wait(ACTION_COOLDOWN)

    # Bring up quick switcher
    pyautogui.hotkey("ctrl", "k")
    _wait(ACTION_COOLDOWN)

    # Input search and enter
    # Note: sometimes this opens the stupid Quick Switcher help webpage
    # and I don't know why
    pyautogui.typewrite(search + "\n")
    _wait(ACTION_COOLDOWN)

    # Focus text area
    pyautogui.hotkey("esc")
    _wait(ACTION_COOLDOWN)
    if verbose:
        rich.print(
            "[bright_black]Finished navigating, focused text area, and ready "
            "to roll[/]"
        )


def _start_rolling(command: str, num: int, daily: bool, verbose: bool) -> None:
    """Repeatedly enter the roll command into the channel.

    Args:
        command (str): The command line argument specifying the name of
        the Mudae command to use to roll for characters. It should be
        unprefixed (no $, /, etc.).
        num (int): The command line argument specifying the number of
        times to roll in this session.
        daily (bool): The command line flag specifying whether the
        daily Mudae commands, $daily and $dailykakera, should be run in
        addition to the rolling this session.
        verbose (bool): Configuration preference.
    """
    if verbose:
        rich.print(f"[bright_black]Starting to roll with {command=}...[/]")
    for attempt_num in range(1, num + 1):
        pyautogui.typewrite(f"${command}\n")
        if verbose:
            rich.print(
                f"[bright_black]Attempted to roll ({attempt_num}/{num})[/]"
            )
        _wait(ROLLING_COOLDOWN)
    if verbose:
        rich.print("[green]Finished rolling[/]")

    if daily:
        pyautogui.typewrite(f"$daily\n")
        _wait(ROLLING_COOLDOWN)
        pyautogui.typewrite(f"$dk\n")
        if verbose:
            rich.print("[green]Finished running daily commands[/]")


def run_autogui(command: str,
                channel: str,
                num: int,
                daily: bool,
                verbose: bool) -> None:
    """Bundle PyAutoGUI actions used to accomplish script.

    Interface function to be called from main process.

    Args:
        command (str): Arg extracted from parser namespace.
        channel (str): Arg extracted from parser namespace.
        num (int): Arg extracted from parser namespace.
        daily (bool): Arg extracted from parser namespace.
        verbose (bool): Configuration preference.
    """
    def pause_callback() -> None:
        global paused
        paused = not paused

    # Register PAUSE_KEY as a hotkey for pausing/resuming this function
    keyboard.add_hotkey(PAUSE_KEY, pause_callback)

    _open_discord(verbose)
    _navigate_to_channel(channel, verbose)
    _start_rolling(command, num, daily, verbose)
