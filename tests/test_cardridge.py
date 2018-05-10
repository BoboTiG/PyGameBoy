"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from pathlib import Path

import pytest

from gameboy.cardridge import Cardridge
from gameboy.exceptions import InvalidRom
from .utils import Swap


@pytest.mark.parametrize('attr, value', [
    ('title', 'Super Mario'),
    ('code', 'Land'),
    ('game_title', 'Super Mario Land'),
    ('mbc_type', 'MBC1'),
    ('rom_size', 64 * 1024),
    ('ram_size', 0),
    ('version', (1, 1)),
    ('header_checksum', 157),
])
def test_attributes(attr, value, cardridge):
    assert getattr(cardridge, attr) == value


def test_repr(cardridge):
    assert repr(cardridge)


def test_validate(cardridge):
    fake = cardridge.data[::4]
    with Swap(cardridge, 'data', fake):
        assert not cardridge.validate()

    path = Path('tests/roms/invalid.gb')
    with pytest.raises(InvalidRom):
        Cardridge(path)
