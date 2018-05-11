"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy

In this file we cannot use a relative import here, else the application will not
start when packaged (see https://github.com/pyinstaller/pyinstaller/issues/2560).
"""

import sys
from pathlib import Path
from typing import List

from gameboy.emulator import Emulator
from gameboy.exceptions import EmulationError


def main(args: List[str]) -> int:
    """This is now we figth!
    Takes only one argument: the ROM file.
    """

    if args:
        rom = Path(args.pop(0))
    else:
        rom = Path("tests/roms/Super Mario Land (JUE) (V1.1) [!].gb")

    try:
        with Emulator(rom) as emu:
            print(f"Starting {emu.cartridge.title} v{emu.cartridge.version}")
            print(emu.cartridge)
            print(emu.cpu)
            print(emu.mmu)
    except EmulationError as exc:
        print(exc)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
