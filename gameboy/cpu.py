"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from typing import List

from . import offset


class CPU:
    """GameBoy CPU Zilog Z80."""

    # Time clock: The Z80 holds two types of clock
    M: int = 0
    T: int = 0

    # Register set
    A: int = 0
    B: int = 0
    C: int = 0
    D: int = 0
    E: int = 0
    F: int = 0
    H: int = 0
    L: int = 0
    PC: int = 0
    SP: int = 0

    def reset(self) -> None:
        """Reset registers and clocks."""
        for attr in "M T A B C D E F H L PC SP".split():
            setattr(self, attr, 0)

    def __repr__(self) -> str:
        state = f"{type(self).__name__}<"
        for attr in "M T A B C D E F H L PC SP".split():
            state += f"{attr}=0x{getattr(self, attr, 0):02X} "
        return state.rstrip() + ">"


class MMU:
    """Memory Management Unit."""

    def __init__(self):
        self.VRAM = self.calloc(offset.VRAM)
        self.ERAM = self.calloc(offset.ERAM)
        self.WRAM = self.calloc(offset.WRAM)
        self.OAM = self.calloc(offset.OAM)
        self.HRAM = self.calloc(offset.HRAM)

    def __repr__(self) -> str:
        return f"{type(self).__name__}<>"

    @staticmethod
    def calloc(size: slice) -> List[int]:
        """Memory allocation."""
        return [0] * (size.stop - size.start)

    def read8(self, addr: int) -> int:
        """Read 8-bit byte from a given address."""

        # TODO: check what is the most taken condition to optimize those branches
        # TODO: refactor with write8()
        if offset.VRAM.start <= addr <= offset.VRAM.stop:
            memory, ptr = self.VRAM, addr - offset.VRAM.start
        elif offset.ERAM.start <= addr <= offset.ERAM.stop:
            memory, ptr = self.ERAM, addr - offset.ERAM.start
        elif offset.WRAM.start <= addr <= offset.WRAM.stop:
            memory, ptr = self.WRAM, addr - offset.WRAM.start
        elif offset.OAM.start <= addr <= offset.OAM.stop:
            memory, ptr = self.OAM, addr - offset.OAM.start
        else:
            memory, ptr = self.HRAM, addr - offset.HRAM.start

        return memory[ptr]

    def write8(self, addr: int, val: int) -> None:
        """Write 8-bit byte to a given address."""

        # TODO: check what is the most taken condition to optimize those branches
        if offset.VRAM.start <= addr <= offset.VRAM.stop:
            memory, ptr = self.VRAM, addr - offset.VRAM.start
        elif offset.ERAM.start <= addr <= offset.ERAM.stop:
            memory, ptr = self.ERAM, addr - offset.ERAM.start
        elif offset.WRAM.start <= addr <= offset.WRAM.stop:
            memory, ptr = self.WRAM, addr - offset.WRAM.start
        elif offset.OAM.start <= addr <= offset.OAM.stop:
            memory, ptr = self.OAM, addr - offset.OAM.start
        else:
            memory, ptr = self.HRAM, addr - offset.HRAM.start

        memory[ptr] = val

    def read16(self, addr: int) -> bytes:
        """Read 16-bit word from a given address."""
        pass

    def write16(self, addr: int, val: int) -> None:
        """Write 16-bit word to a given address."""
        pass
