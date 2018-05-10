"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from pathlib import Path

from gameboy.cartridge import Cartridge

import pytest


@pytest.fixture(scope='session')
def cartridge():
    path = Path('tests/roms/Super Mario Land (JUE) (V1.1) [!].gb')
    return Cartridge(path)
