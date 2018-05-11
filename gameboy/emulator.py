"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from pathlib import Path

from . import offset
from .cartridge import Cartridge
from .cpu import CPU, MMU
from .debug import hexdump


class Emulator:
    """Operations center."""

    def __init__(self, rom: Path):
        self.cartridge = Cartridge(rom)
        self.cpu = CPU()
        self.mmu = MMU()
        self.prog = memoryview(self.cartridge.data[offset.USER_PROG])

        # """
        print(hexdump(self.prog))
        for n, op in enumerate(self.prog):
            if n == 10:
                break
            print(f"0x{op:02X} {op}")
        # """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
