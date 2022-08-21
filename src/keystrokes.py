"""
keystrokes.py
20 August 2022 13:13:59

The bulk of the pyautogui calls.
"""

import time

import keyboard
import pyautogui
import rich

# todo: Make configurable later
# The sleep calls are to prevent potential latency problems
# and to not appear suspicious.
ACTION_COOLDOWN = 0.1  # seconds to wait between actions
TYPING_COOLDOWN = 0.05  # seconds to wait between character input
ROLLING_COOLDOWN = 1.0  # seconds to wait between waifu roll attempts


def wait_for_ready() -> None:
    """Block until the ENTER key is pressed."""
    rich.print(
        "[bold yellow]Hit ENTER when application is finished loading "
        "to start the keystroke sequences[/]"
    )
    keyboard.wait("enter")


def navigate_to_channel(channel: str) -> None:
    """Navigate to the target channel within Discord to roll in.

    This function does not guarantee that focus is brought to the
    desired channel is the argument is ill-defined.

    Args:
        channel (str): The command line argument that specifies the
        query string to submit to the Discord search bar to locate the
        channel to roll in.
    """
    # In case user put the # in there themselves
    search = "#" + channel.removeprefix("#")
    rich.print(
        "[bright_black]Navigating by searching for channel with query "
        f"{search!r}...[/]"
    )

    # In case search bar was already up for some reason
    pyautogui.hotkey("esc")
    time.sleep(ACTION_COOLDOWN)

    # Bring up quick switcher
    pyautogui.hotkey("ctrl", "k")
    time.sleep(ACTION_COOLDOWN)

    # Input search and enter
    # Note: sometimes this opens the stupid Quick Switcher help webpage
    # and I don't know why
    pyautogui.typewrite(search + "\n", interval=TYPING_COOLDOWN)
    time.sleep(ACTION_COOLDOWN)

    # Focus text area
    pyautogui.hotkey("esc")
    time.sleep(ACTION_COOLDOWN)
    rich.print(
        "[bright_black]Finished navigating, focused text area, and ready to "
        "roll[/]"
    )


def start_rolling(command: str, num: int, daily: bool) -> None:
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
    """
    rich.print(f"[bright_black]Starting to roll with {command=}...[/]")
    for attempt_num in range(1, num + 1):
        pyautogui.typewrite(f"${command}\n")
        rich.print(
            f"[bright_black]Attempted to roll ({attempt_num}/{num})[/]"
        )
        time.sleep(ROLLING_COOLDOWN)
    rich.print("[green]Finished rolling[/]")

    if daily:
        pyautogui.typewrite(f"$daily\n")
        time.sleep(ROLLING_COOLDOWN)
        pyautogui.typewrite(f"$dk\n")
        rich.print("[green]Finished running daily commands[/]")
