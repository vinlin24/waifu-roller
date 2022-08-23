"""
abort.py
20 August 2022 21:52:36

Handles program behavior upon forceful termination.
"""

import _thread
import signal
import sys
from types import FrameType
from typing import NoReturn

import keyboard
import pyautogui
import rich

ABORT_KEY = "esc"


def _custom_abort_callback() -> NoReturn:
    """Attempt to exit the program by interrupting main thread.

    It does this by sending signal SIGINT to the main thread from the
    current (listener) thread, then exiting the thread.

    Raises:
        SystemExit: Exit the current thread silently.
    """
    rich.print(f"[bold red]Script interrupted with {ABORT_KEY.upper()} key[/]")
    # sys.exit() only interrupts keyboard listener thread
    _thread.interrupt_main()
    _thread.exit()


def _interrupt_handler(sig: int, frame: FrameType | None) -> NoReturn:
    """Callback to pass to signal.signal for SIGINT.

    Args:
        sig (int): Signal number, required parameter.
        frame (FrameType | None): Stack frame, required parameter.

    Raises:
        SystemExit: Exits the program with sys.exit
    """
    rich.print("[bold red]Script terminated by SIGINT[/]")
    sys.exit()


def register_abort_handlers(failsafe: bool) -> None:
    """Set up signal and hotkey listeners for program abortion.

    Args:
        failsafe (bool): Configuration preference.

    Interface function to be called from main process.
    """
    signal.signal(signal.SIGINT, _interrupt_handler)
    # Set up custom abort handler
    keyboard.add_hotkey(ABORT_KEY, _custom_abort_callback)
    # Suppress pyautogui failsafe based on config
    pyautogui.FAILSAFE = failsafe
