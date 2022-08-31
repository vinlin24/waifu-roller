"""
core.py
20 August 2022 13:13:59

The bulk of the pyautogui calls.
"""

import signal
import time

import keyboard
import pyautogui
import rich

from waifu.abort import ABORT_KEY
from waifu.exceptions import DiscordNotOpenError

# todo: Make configurable later? maybe not
# The sleep calls are to prevent potential latency problems
# and to not appear suspicious.
ACTION_COOLDOWN = 0.1  # seconds to wait between actions
TYPING_COOLDOWN = 0.05  # seconds to wait between character input
ROLLING_COOLDOWN = 1.0  # seconds to wait between waifu roll attempts

PAUSE_KEY = "capslock"
REVERT_WINDOW_DELAY = 3.0  # seconds to wait before reverting window


class _Pauser:
    """Global flag manager for if autogui process is paused or not."""
    paused = False

    @classmethod
    def toggle(cls, verbose: bool) -> None:
        """Toggle the internal flag."""
        cls.paused = not cls.paused
        if cls.paused:
            rich.print("[yellow]Program has been paused.[/]")
        else:
            rich.print("[yellow]Program resumed.[/]")
            # 0.0.4: Move back to Discord if unfocused
            if not _is_discord_active():
                _open_discord(verbose)
                _wait(0.1)


def _is_discord_active() -> bool:
    title: str | None = pyautogui.getActiveWindowTitle()
    return (title is not None and
            (title == "Discord" or title.endswith("- Discord")))


def _wait(delay: float) -> None:
    """Wait for at least delay seconds and some conditions.

    After waiting for delay seconds, wait for after the paused flag is
    False and the Discord window is the active window.

    Args:
        delay (float): Minimum time in seconds to wait.
    """
    time.sleep(delay)
    # 0.0.4: Notify if Discord window lost focus
    if not _is_discord_active():
        rich.print(
            "[bright_black]Discord not in focus, program suspended...[/]"
        )
    # Block until unpaused and focused
    while _Pauser.paused or not _is_discord_active():
        pass


def _open_discord(verbose: bool) -> None:
    """Move to the Discord desktop application.

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
    pyautogui.typewrite(search + "\n", interval=TYPING_COOLDOWN)
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
        rich.print("[green]Finished rolling.[/]")

    if daily:
        pyautogui.typewrite(f"$daily\n")
        _wait(ROLLING_COOLDOWN)
        pyautogui.typewrite(f"$dk\n")
        if verbose:
            rich.print("[green]Finished running daily commands.[/]")


def _revert_window(win: pyautogui.Window, verbose: bool) -> None:
    """Restore focus to the window script was called from.

    Args:
        win (pyautogui.Window): The window to restore focus to.
        verbose (bool): Configuration preference.
    """
    if verbose:
        rich.print(
            "[bright_black]"
            f"Waiting for a delay of {REVERT_WINDOW_DELAY} seconds "
            f"before restoring your window '{win.title}'"
            "[/]\n"
            "[yellow]"
            "[TIP] You can cancel the window focus change with the "
            f"{ABORT_KEY.upper()} hotkey during this delay if you want "
            "to react to a Mudae message or review your rolls."
            "[/]"
        )
    _wait(REVERT_WINDOW_DELAY)
    win.activate()
    if verbose:
        rich.print(
            f"[bright_black]Returned focus to window '{win.title}'"
        )


def _raise_corner_abort() -> None:
    """Customize behavior of pyautogui.FailSafeException."""
    rich.print(
        "\n[bold red]"
        "Fail-safe triggered from mouse moving to a corner of the screen.[/]\n"
        "[TIP] To disable this fail-safe, you can set the [blue]keep-failsafe"
        "[/] option to [red]false[/] in your configuration file.\n"
    )
    signal.raise_signal(signal.SIGINT)


def run_autogui(command: str,
                channel: str,
                num: int,
                daily: bool,
                verbose: bool,
                revert: bool) -> None:
    """Bundle PyAutoGUI actions used to accomplish script.

    Interface function to be called from main process.

    Args:
        command (str): Arg extracted from parser namespace.
        channel (str): Arg extracted from parser namespace.
        num (int): Arg extracted from parser namespace.
        daily (bool): Arg extracted from parser namespace.
        verbose (bool): Configuration preference.
        revert (bool): Configuration preference.
    """
    # Register PAUSE_KEY as a hotkey for pausing/resuming this function
    keyboard.add_hotkey(PAUSE_KEY, _Pauser.toggle, (verbose,))

    try:
        caller_win = pyautogui.getActiveWindow()

        _open_discord(verbose)
        _navigate_to_channel(channel, verbose)
        _start_rolling(command, num, daily, verbose)

        # Restore window script was called from if configured
        if revert and caller_win is not None:
            _revert_window(caller_win, verbose)
    except pyautogui.FailSafeException:
        _raise_corner_abort()
