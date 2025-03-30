"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from pathlib import Path
from types import SimpleNamespace

import pytest

from gameboy.cartridge import Cartridge
from gameboy.exceptions import InvalidRomError, InvalidZipError
from gameboy.offset import GLOBAL_CHECKSUM


@pytest.mark.parametrize(
    ("attr", "value"),
    [
        ("title", "SUPER MARIOLAND"),
        ("code", "LAND"),
        ("cgb_flag", False),
        ("licensee", ""),
        ("sgb_flag", False),
        ("type", "MBC1"),
        ("rom_size", "64KB"),
        ("ram_size", "0KB"),
        ("destination", "Japan"),
        ("old_licensee", "01"),
        ("version", 1.1),
        ("header_checksum", True),
        ("global_checksum", True),
        ("publisher", "Nintendo"),
    ],
)
def test_attributes(attr: str, value: bool, cartridge: Cartridge) -> None:
    """Test cartridge attributes."""
    assert getattr(cartridge, attr) == value


def test_logo(cartridge: Cartridge) -> None:
    """Test the Nintendo logo is well formatted."""
    assert cartridge.logo == (
        b"\xce\xedff\xcc\r\x00\x0b\x03s\x00\x83\x00\x0c\x00\r\x00\x08\x11\x1f"
        b"\x88\x89\x00\x0e\xdc\xccn\xe6\xdd\xdd\xd9\x99\xbb\xbbgcn\x0e\xec\xcc"
        b"\xdd\xdc\x99\x9f\xbb\xb93>"
    )


def test_parse(cartridge: Cartridge) -> None:
    """Test cartridge parse()."""
    details = cartridge.parse()
    assert isinstance(details, SimpleNamespace)
    assert details.cgb is False
    assert details.destination == "Japan"
    assert details.file == cartridge.rom
    assert details.licensee == ""
    assert details.old_licensee == "01"
    assert details.publisher == "Nintendo"
    assert details.ram_size == "0KB"
    assert details.rom_size == "64KB"
    assert details.sgb is False
    assert details.title == "SUPER MARIOLAND"
    assert details.type == "MBC1"
    assert details.valid is True
    assert details.valid_complete is True
    assert details.version == 1.1


def test_parse_error(mario: Path) -> None:
    """Test a ROM with truncated headers."""
    with mario.open("rb") as source:
        # Read the minimum data required to pass the validation
        # but not enough for the parser to fully work
        data = source.read(GLOBAL_CHECKSUM.start)

    cartridge = Cartridge(data)
    with pytest.raises(InvalidRomError) as exc:
        cartridge.parse()
    assert "parsing error" in str(exc.value)


def test_title_unicode(roms: Path) -> None:
    """Test a ROM containing non-ascii letters in its title."""
    rom = roms / "Pocket Monsters Yellow (J) (V1.0) (S)(T+Eng_BinHN).zip"
    cartridge = Cartridge(rom)
    assert cartridge.title == "POKÉMON YELLOW"


def test_repr(cartridge: Cartridge) -> None:
    """Test cartridge repr()."""
    assert repr(cartridge)


def test_is_completely_valid(cartridge: Cartridge) -> None:
    """Test cartridge validation."""
    assert cartridge.is_valid(complete=True)


def test_invalid_rom(roms: Path) -> None:
    """Test cartridge validation with an invalid ROM."""
    rom = roms / "invalid.gb"
    cartridge = Cartridge(rom)
    assert not cartridge.is_valid()


def test_rom_with_licensee(roms: Path) -> None:
    """Test a ROM with no old licensee but licensee."""
    rom = roms / "Gameboy Camera Gold - Zelda Edition (U) (S).zip"
    cartridge = Cartridge(rom)
    assert cartridge.licensee == "01"
    assert cartridge.publisher == "Nintendo"


def test_rom_is_bytes(mario: Path) -> None:
    """Test the emulator can run with in-memory bytes."""
    rom = mario.read_bytes()
    cartridge = Cartridge(rom)
    assert "SUPER MARIOLAND" in repr(cartridge)


def test_rom_is_str(roms: Path) -> None:
    """Test the emulator can open a ZIP file containing a ROM."""
    rom = str(roms / "Super Mario Land (W) (V1.1).zip")
    cartridge = Cartridge(rom)
    assert "SUPER MARIOLAND" in repr(cartridge)


def test_rom_is_zip(roms: Path) -> None:
    """Test the emulator can open a ZIP file containing a ROM."""
    rom = roms / "Super Mario Land (W) (V1.1).zip"
    cartridge = Cartridge(rom)
    assert "SUPER MARIOLAND" in repr(cartridge)


def test_rom_is_zip_but_contains_no_rom(roms: Path) -> None:
    """Test a ZIP file containing no ROM."""
    rom = roms / "README.md.zip"
    with pytest.raises(InvalidZipError) as exc:
        Cartridge(rom)
    assert str(exc.value)
