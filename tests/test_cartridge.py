"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from pathlib import Path

import pytest
from gameboy.cartridge import Cartridge
from gameboy.exceptions import InvalidRom, InvalidZip


@pytest.mark.parametrize(
    "attr, value",
    [
        ("title", "SUPER MARIOLAND"),
        ("version", 1.1),
        ("cgb_flag", False),
        ("publisher", "Nintendo"),
        ("sgb_flag", False),
        ("type", "MBC1"),
        ("rom_size", "64KB"),
        ("ram_size", "0KB"),
        ("destination", "Japan"),
        ("logo", True),
        ("license", ""),
        ("old_license", "01"),
    ],
)
def test_attributes(attr, value, cartridge):
    """Test cartridge attributes."""
    assert getattr(cartridge, attr) == value


def test_parse(cartridge):
    """Test cartridge parse()."""
    assert cartridge.parse() == {
        "CGB flag": False,
        "RAM size": "0KB",
        "ROM size": "64KB",
        "SGB flag": False,
        "destination": "Japan",
        "global checksum": False,
        "header checksum": True,
        "path": Path("tests/roms/Super Mario Land (JUE) (V1.1) [!].gb"),
        "publisher": "Nintendo",
        "title": "SUPER MARIOLAND",
        "type": "MBC1",
        "version": 1.1,
    }


def test_parse_error():
    """Test a ROM with truncated headers.
    To create the bad file:
        $ cp "Super Mario Land (JUE) (V1.1) [!].gb" corrupted-headers.gb
        $ truncate -s 334 corrupted-headers.gb
    """
    path = path = Path("tests/roms/corrupted-headers.gb")
    with pytest.raises(InvalidRom):
        Cartridge(path)


def test_title_unicode():
    """Test a ROM containing non-ascii letters in its title."""
    path = Path("tests/roms/Pocket Monsters Yellow (J) (V1.0) (S)(T+Eng_BinHN).zip")
    cartridge = Cartridge(path)
    assert cartridge.title == "POKÉMON YELLOW"


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
    assert "SUPER MARIOLAND" in repr(cartridge)


def test_zip_no_rom():
    """Test a ZIP file containing no ROM."""
    path = Path("tests/roms/README.md.zip")
    with pytest.raises(InvalidZip) as exc:
        Cartridge(path)
    assert str(exc.value)
