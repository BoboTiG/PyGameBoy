"""
This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

# Cardridge offsets
ENTRY_POINT = slice(0x100, 0x103 + 1)  # type: slice
LOGO = slice(0x104, 0x133 + 1)  # type: slice
TITLE = slice(0x134, 0x143 + 1)  # type: slice
MANUFACTURER = slice(0x13F, 0x142 + 1)  # type: slice
CBG_FLAG = 0x143  # type: int
LICENSE = slice(0x144, 0x145 + 1)  # type: slice
SBG_FLAG = 0x146  # type: int
TYPE = 0x147  # type: int
ROM_SIZE = 0x148  # type: int
RAM_SIZE = 0x149  # type: int
DEST_CODE = 0x14A  # type: int
OLD_LICENSE = 0x14B  # type: int
VERSION = 0x14C  # type: int
HEADER_CHECKSUM = 0x14D  # type: int
GLOBAL_CHECKSUM = slice(0x14E, 0x14F + 1)  # type: slice
