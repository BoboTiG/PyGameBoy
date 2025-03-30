"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from collections.abc import Sequence
from itertools import zip_longest

__all__ = ("hexdump",)


def grouper(iterable: bytes, count: int) -> Sequence[tuple[bytes, ...]]:
    """Collect data into fixed-length chunks or blocks.
    grouper(b'ABCDEFG', 3) --> b'ABC' b'DEF' b'G'.
    """
    args = [iter(iterable)] * count
    return zip_longest(*args)  # type: ignore[return-value]


def hexdump(data: bytes) -> str:
    """Display binary data like in a real hexeditor."""
    dump = []
    for seq in grouper(data, 16):
        subdump = [f"{val:02X}" for val in seq if val is not None]  # type: ignore[str-bytes-safe]
        dump.append(" ".join(subdump))
    return "\n".join(dump)
