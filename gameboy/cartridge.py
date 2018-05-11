"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from pathlib import Path

from . import offset
from .exceptions import InvalidRom


class Cartridge:
    """Cartridge content."""

    __title: str = ''
    __version: str = ''

    def __init__(self, path: Path) -> None:
        with open(path, 'rb') as card:
            self.data: bytes = card.read()

        if not self.validate():
            raise InvalidRom()

    def __repr__(self) -> str:
        return (f'{type(self).__name__}<id=0x{id(self)}, title={self.title!r}'
                f', version={self.version!r}>')

    @property
    def title(self) -> str:
        """Game title."""

        if not self.__title:
            self.__title = self.data[offset.TITLE].decode().rstrip('\0')
            code = self.data[offset.CODE].decode().rstrip('\0')
            if code:
                self.__title += f' {code}'
            self.__title = self.__title.title()
        return self.__title

    @property
    def version(self) -> str:
        """ROM version."""

        if not self.__version:
            self.__version = f'1.{self.data[offset.VERSION]}'
        return self.__version

    def validate(self) -> bool:
        """Verify the header validity."""

        checksum: int = 0
        for value in self.data[offset.TITLE.start:offset.VERSION + 1]:
            checksum = checksum - value - 1
        checksum &= 0xFF
        return checksum == self.data[offset.HEADER_CHECKSUM]
