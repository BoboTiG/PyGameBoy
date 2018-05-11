"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

# Interrupts
RST = slice(0x000, 0x0FF + 1)

# ROM data
ENTRY_POINT = slice(0x100, 0x103 + 1)
LOGO = slice(0x104, 0x133 + 1)
TITLE = slice(0x134, 0x13E + 1)
CODE = slice(0x13F, 0x142 + 1)
CBG_FLAG = 0x143
LICENSE = slice(0x144, 0x145 + 1)
SBG_FLAG = 0x146
TYPE = 0x147
ROM_SIZE = 0x148
RAM_SIZE = 0x149
DEST_CODE = 0x14A
VERSION = 0x14C
HEADER_CHECKSUM = 0x14D
GLOBAL_CHECKSUM = slice(0x14E, 0x14F + 1)
USER_PROG = slice(0x150, 0x7FFF + 1)

# Memory
VRAM = slice(0x8000, 0x9FFF + 1)  # Video RAM
ERAM = slice(0xA000, 0xBFFF + 1)  # External RAM
WRAM = slice(0xC000, 0xDFFF + 1)  # Work RAM
OAM = slice(0xFE00, 0xFE9F + 1)  # Sprite attribute table
HRAM = slice(0xFF80, 0xFFFE + 1)  # High RAM

# I/O ports
P1, SB, SC, DIV, TIMA, TMA, TAC = range(0xFF00, 0xFF07)

# Interrupt enable register
IE = 0xFFFF
