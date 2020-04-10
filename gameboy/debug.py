"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from itertools import zip_longest
from typing import Any, Sequence


__all__ = ("hexdump",)


def grouper(iterable: Sequence, count: int, fillvalue: Any = None):
    """"Collect data into fixed-length chunks or blocks.
        grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    """
    args = [iter(iterable)] * count
    return zip_longest(*args, fillvalue=fillvalue)


def hexdump(data: bytes) -> str:
    """Display binary data like in a real hexeditor."""
    dump = []
    for seq in grouper(data, 16):
        subdump = [f"{val:02X}" for val in seq if val is not None]
        dump.append(" ".join(subdump))
    return "\n".join(dump)
