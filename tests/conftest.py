"""
This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from pathlib import Path

from gameboy.cardridge import Cardridge

import pytest


@pytest.fixture(scope='session')
def cardridge(rom):
    return Cardridge(rom)


@pytest.fixture(scope='session')
def data(cardridge):
    return cardridge.data


@pytest.fixture(scope='session')
def rom():
    return Path('tests/roms/Super Mario Land (JUE) (V1.1) [!].gb')
