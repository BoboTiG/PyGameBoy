"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from pathlib import Path

import pytest
from gameboy.cartridge import Cartridge
from gameboy.exceptions import InvalidRom

from .utils import Swap


@pytest.mark.parametrize(
    "attr, value", [("title", "Super Mario Land"), ("version", "1.1")]
)
def test_attributes(attr, value, cartridge):
    """Test cartridge attributes."""
    assert getattr(cartridge, attr) == value


def test_repr(cartridge):
    """Test cartridge repr()."""
    assert repr(cartridge)


def test_validate(cartridge):
    """Test cartridge validation."""
    fake = cartridge.data[::4]
    with Swap(cartridge, "data", fake):
        assert not cartridge.validate()

    path = Path("tests/roms/invalid.gb")
    with pytest.raises(InvalidRom) as exc:
        Cartridge(path)
    assert str(exc.value)
