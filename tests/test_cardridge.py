"""
This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

import pytest


@pytest.mark.parametrize('attr, value', [
    ('title', 'SUPER MARIOLAND'),
    ('manufacturer', 'LAND'),
    ('license', ''),
    ('old_license', '\x01'),
    ('type', '\x01'),
    ('rom_size', '\x01'),
    ('ram_size', ''),
    ('dest_code', ''),
    ('version', '\x01'),
    ('header_checksum', '\x9d'),
    ('global_checksum', '^Ï'),
])
def test_attributes(attr, value, cardridge):
    assert getattr(cardridge, attr) == value
