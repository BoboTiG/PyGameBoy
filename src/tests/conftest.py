"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from pathlib import Path

import pytest

from gameboy.cartridge import Cartridge


@pytest.fixture(scope="session")
def roms() -> Path:
    """The folder containing all test ROMs."""
    return Path(__file__).parent / "roms"


@pytest.fixture(scope="session")
def mario(roms: Path) -> Path:
    """The GameBoy ROM file of Super Mario Land."""
    return roms / "Super Mario Land (JUE) (V1.1) [!].gb"


@pytest.fixture(scope="session")
def cartridge(mario: Path) -> Cartridge:
    """A real ROM for our tests."""
    return Cartridge(mario)
