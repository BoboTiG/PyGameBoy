"""
This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from pathlib import Path
from typing import Union

from . import constants


class Cardridge:
    """ Cardridge content. """

    def __init__(self, path: Union[str, Path]) -> None:
        if not isinstance(path, Path):
            path = Path(path)

        with open(path, 'rb') as card:
            self.data = card.read()  # type: bytes

    def __getattr__(self, item: str) -> Union[str, bytes]:
        try:
            offset = getattr(constants, item.upper())
        except AttributeError:
            # It must be self.data only
            return self.__dict__[item]  # type: bytes
        else:
            if isinstance(offset, slice):
                data = ''.join(map(chr, self.data[offset]))  # type: str
            else:
                data = chr(self.data[offset])
            return data.rstrip('\0')  # type: str
