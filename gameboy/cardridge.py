"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from pathlib import Path

from . import offset
from .exceptions import InvalidRom


class Cardridge:
    """Cardridge content."""

    __slots__ = ('data', 'title', 'version')

    def __init__(self, path: Path) -> None:
        with open(path, 'rb') as card:
            self.data: bytes = card.read()

        if not self.validate():
            raise InvalidRom('Invalid header checksum')

        # Game properties
        self.title: str = ' '.join((
            self.data[offset.TITLE].decode().rstrip('\0'),
            self.data[offset.CODE].decode().rstrip('\0'))).title()
        self.version: str = f'1.{self.data[offset.VERSION]}'

    def __repr__(self) -> str:
        return (f'{type(self).__name__}<id=0x{id(self)}, title={self.title!r}'
                f', version={self.version!r}>')

    def validate(self) -> bool:
        """Verify the header validity."""
        checksum: int = 0
        for value in self.data[0x134:0x14C + 1]:
            checksum = checksum - value - 1
        checksum &= 0xFF
        return checksum == self.data[offset.HEADER_CHECKSUM]
