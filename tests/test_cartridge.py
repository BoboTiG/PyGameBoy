"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from pathlib import Path

import pytest
from gameboy.cartridge import Cartridge
from gameboy.exceptions import InvalidRom, InvalidZip


@pytest.mark.parametrize(
    "attr, value", [("title", "Super Mario Land"), ("version", "1.1")]
)
def test_attributes(attr, value, cartridge):
    """Test cartridge attributes."""
    assert getattr(cartridge, attr) == value


def test_repr(cartridge):
    """Test cartridge repr()."""
    assert repr(cartridge)


def test_validate():
    """Test cartridge validation."""
    path = Path("tests/roms/invalid.gb")
    with pytest.raises(InvalidRom) as exc:
        Cartridge(path)
    assert str(exc.value)


def test_zip():
    """Test the emulator can open a ZIP file containing a ROM."""
    path = Path("tests/roms/Super Mario Land (W) (V1.1).zip")
    cartridge = Cartridge(path)
    assert "Super Mario Land" in repr(cartridge)


def test_zip_no_rom():
    """Test a ZIP file containing no ROM."""
    path = Path("tests/roms/README.md.zip")
    with pytest.raises(InvalidZip) as exc:
        Cartridge(path)
    assert str(exc.value)
