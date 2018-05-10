"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

# ROM Registration Data
ENTRY_POINT: slice = slice(0x100, 0x103 + 1)
LOGO: slice = slice(0x104, 0x133 + 1)
TITLE: slice = slice(0x134, 0x13E + 1)
CODE: slice = slice(0x13F, 0x142 + 1)
CBG_FLAG: int = 0x143
LICENSE: slice = slice(0x144, 0x145 + 1)
SBG_FLAG: int = 0x146
TYPE: int = 0x147
ROM_SIZE: int = 0x148
RAM_SIZE: int = 0x149
DEST_CODE: int = 0x14A
VERSION: int = 0x14C
HEADER_CHECKSUM: int = 0x14D
GLOBAL_CHECKSUM: slice = slice(0x14E, 0x14F + 1)
