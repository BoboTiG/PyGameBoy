"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from pathlib import Path

from . import offset
from .exceptions import InvalidRom


class Cardridge:
    """Cardridge content."""

    def __init__(self, path: Path) -> None:
        with open(path, 'rb') as card:
            self.data: bytes = card.read()

        if not self.validate():
            raise InvalidRom('Invalid header checksum')

    def __repr__(self) -> str:
        return f'{type(self).__name__}<id={id(self)}, title={self.title!r}>'

    @property
    def title(self) -> str:
        """Title of the game in UPPER CASE ASCII.
        If it is less than 16 characters then the remaining bytes are
        filled with 00's.
        """
        return ''.join(map(chr, self.data[offset.TITLE])).rstrip('\0')

    @property
    def rom_size(self) -> int:
        """ROM Size."""
        val = f'0x{self.data[offset.ROM_SIZE]:02x}'
        return {
            '0x00': 32 * 1024,
            '0x01': 64 * 1024,
            '0x02': 128 * 1024,
            '0x03': 256 * 1024,
            '0x04': 512 * 1024,
            '0x05': 1024 * 1024,
            '0x06': 2048 * 1024,
            '0x07': 4096 * 1024,
            '0x52': 1024 * 1024 + 128 * 1024,
            '0x53': 1024 * 1024 + 256 * 1024,
            '0x54': 1024 * 1024 + 512 * 1024,
        }.get(val)

    @property
    def ram_size(self) -> int:
        """RAM Size."""
        val = f'0x{self.data[offset.RAM_SIZE]:02x}'
        return {
            '0x00': 0,
            '0x01': 2 * 1024,
            '0x02': 8 * 1024,
            '0x03': 32 * 1024,
        }.get(val)

    @property
    def header_checksum(self) -> int:
        """Header Checksum.
        Contains an checksum across the cartridge header bytes 0134-014C.
        The lower 8 bits of the result must be the same than the value
        in this entry.
        The game _will not work _ if this checksum is incorrect.
        """
        return int(self.data[offset.HEADER_CHECKSUM])

    def validate(self) -> bool:
        """Verify the header validity."""
        checksum: int = 0
        for i in self.data[0x134:0x14C + 1]:
            checksum = checksum - i - 1
        checksum &= 0xFF
        return checksum == self.header_checksum
