"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from itertools import zip_longest
from typing import Any, Sequence


__all__ = ('hexdump',)


def grouper(iterable: Sequence, n: int, fillvalue: Any=None):
    """"
    Collect data into fixed-length chunks or blocks.
        grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def hexdump(data: bytes) -> str:
    """ Display binary data like in a real hexeditor. """

    r = []
    for h in grouper(data, 16):
        aa = []
        for hh in h:
            if hh is not None:
                aa.append(f'{hh:02X}')
        r.append(' '.join(aa))
    return '\n'.join(r)
