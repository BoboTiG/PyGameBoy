"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from pathlib import Path
from typing import Tuple

from . import offset
from .exceptions import InvalidRom


class Cardridge:
    """Cardridge content."""

    def __init__(self, path: Path) -> None:
        with open(path, 'rb') as card:
            self.__data: bytes = card.read()

        self.data: memoryview = memoryview(self.__data)

        if not self.validate():
            raise InvalidRom('Invalid header checksum')

    def __repr__(self) -> str:
        return f'{type(self).__name__}<id={id(self)}, title={self.title!r}>'

    @property
    def title(self) -> str:
        """Title of the game."""
        return ''.join(map(chr, self.data[offset.TITLE])).rstrip('\0').title()

    @property
    def mbc_type(self) -> str:
        """Cartridge Type."""
        return {
            0x00: 'ROMO',
            0x01: 'MBC1',
            0x05: 'MBC2',
            0x11: 'MBC3',
            0x19: 'MBC5',
        }.get(self.data[offset.TYPE])

    @property
    def rom_size(self) -> int:
        """ROM Size."""
        return {
            0x00: 32 * 1024,
            0x01: 64 * 1024,
            0x02: 128 * 1024,
            0x03: 256 * 1024,
            0x04: 512 * 1024,
            0x05: 1024 * 1024,
            0x06: 2048 * 1024,
            0x07: 4096 * 1024,
            0x52: 1024 * 1024 + 128 * 1024,
            0x53: 1024 * 1024 + 256 * 1024,
            0x54: 1024 * 1024 + 512 * 1024,
        }.get(self.data[offset.ROM_SIZE])

    @property
    def ram_size(self) -> int:
        """RAM Size."""
        return {
            0x00: 0,
            0x01: 2 * 1024,
            0x02: 8 * 1024,
            0x03: 32 * 1024,
        }.get(self.data[offset.RAM_SIZE])

    @property
    def version(self) -> Tuple[int, int]:
        """Header Checksum."""
        return 1, int(self.data[offset.VERSION])

    @property
    def header_checksum(self) -> int:
        """Header Checksum."""
        return int(self.data[offset.HEADER_CHECKSUM])

    def validate(self) -> bool:
        """Verify the header validity."""
        checksum: int = 0
        for i in self.data[0x134:0x14C + 1]:
            checksum = checksum - i - 1
        checksum &= 0xFF
        return checksum == self.header_checksum
