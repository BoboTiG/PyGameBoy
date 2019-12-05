"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from pathlib import Path

import pytest
from gameboy.cartridge import Cartridge


@pytest.fixture(scope="session")
def roms():
    """The folder containing all test ROMs."""
    return Path("tests") / "roms"


@pytest.fixture(scope="session")
def mario(roms):
    """The GameBoy ROM file of Super Mario Land."""
    # pylint: disable=redefined-outer-name
    return roms / "Super Mario Land (JUE) (V1.1) [!].gb"


@pytest.fixture(scope="session")
def cartridge(mario):
    """A real ROM for our tests."""
    # pylint: disable=redefined-outer-name
    return Cartridge(mario)
