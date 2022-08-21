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
import rich


def _custom_abort_callback() -> NoReturn:  # type: ignore
    """Attempt to exit the program by interrupting main thread.

    Raises:
        KeyboardInterrupt: Sends signal SIGINT to main thread.
    """
    rich.print("[bold red]Script interrupted with TAB key[/]")
    # sys.exit() only interrupts keyboard listener thread
    _thread.interrupt_main()


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


def register_abort_handlers() -> None:
    """Set up signal and hotkey listeners for program abortion.

    Interface function to be called from main process.
    """
    signal.signal(signal.SIGINT, _interrupt_handler)
    # Set up custom abort handler
    keyboard.add_hotkey("tab", _custom_abort_callback)
    rich.print(
        "[bold yellow]Abort the script at any time with the TAB key[/]"
    )
