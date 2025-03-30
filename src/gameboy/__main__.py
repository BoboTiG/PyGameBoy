"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy

In this file we cannot use a relative import here, else the application will not
start when packaged (see https://github.com/pyinstaller/pyinstaller/issues/2560).
"""

import os
import sys
from functools import lru_cache
from os.path import expandvars
from pathlib import Path

from gameboy.cartridge import Cartridge


@lru_cache(maxsize=1)
def supports_color() -> bool:
    """Return True if the running system's terminal supports color, and False otherwise.
    Source: https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != "Pocket PC" and (plat != "win32" or "ANSICON" in os.environ)

    # isatty() is not always implemented
    is_a_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
    return supported_platform and is_a_tty and "NOCOLORS" not in os.environ


# Terminal colors
NONE = "\033[0m" if supports_color() else ""
GREEN = "\033[32m" if supports_color() else ""
RED = "\033[31m" if supports_color() else ""
YELLOW = "\033[33m" if supports_color() else ""
MAGENTA = "\033[35m" if supports_color() else ""


def check(rom: Path) -> int:
    """Check the ROM validity."""
    cartridge = Cartridge(rom)
    if not cartridge.is_valid(complete=True):
        print(f"[{RED}NG{NONE}]", rom.name)
        return 1
    print(f"[{GREEN}OK{NONE}]", rom.name)
    return 0


def dump(rom: Path) -> int:
    """Print ROM headers."""
    cartridge = Cartridge(rom)
    for header, value in cartridge.parse().__dict__.items():
        # Fancy colors!
        if isinstance(value, bool):
            color = GREEN if value else RED
        elif isinstance(value, (int, float)):
            color = MAGENTA
        else:
            color = YELLOW

        print(f"{NONE}{header.ljust(16, '.')}{NONE}", f"{color}{value}{NONE}")
    return 0


def usage() -> int:
    """Print the usage."""
    print(f"Usage: pygameboy {GREEN}FILE{NONE} [{YELLOW}ACTION{NONE}]")
    print()
    print(f"Possible {YELLOW}ACTION{NONE}:")
    print(f"  {YELLOW}check{NONE}: check the ROM {GREEN}FILE{NONE} integrity.")
    print(f"  {YELLOW}dump{NONE} : print ROM {GREEN}FILE{NONE} headers.")
    return -1


def main(file: Path | str, action: str) -> int:
    """Entry point."""
    # Resolve shell variables and ~
    rom = Path(expandvars(file)).expanduser()

    match action:
        case "check":
            return check(rom)
        case "dump":
            return dump(rom)
        case _:
            msg = f"Invalid {action =}"
            raise ValueError(msg)


if __name__ == "__main__":  # pragma: nocover
    if len(sys.argv) < 3:
        sys.exit(usage())
    sys.exit(main(*sys.argv[1:]))
