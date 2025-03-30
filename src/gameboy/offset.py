"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

# Interrupts
RST = slice(0x000, 0x100)

#
# ROM data
#

# Cartridge Header in First ROM Bank
# The memory at 0100-014F contains the cartridge header. This area contains
# information about the program, its entry point, checksums, information about
# the used MBC chip, the ROM and RAM sizes, etc. Most of the bytes in this area
# are required to be specified correctly.

# 0100-0103 - Entry Point
# After displaying the Nintendo Logo, the built-in boot procedure jumps to this
# address (100h), which should then jump to the actual main program in the
# cartridge. Usually this 4 byte area contains a NOP instruction, followed by a
# JP 0150h instruction. But not always.
ENTRY_POINT = slice(0x100, 0x104)

# 0104-0133 - Nintendo Logo
LOGO = slice(0x104, 0x134)

# 0134-0143 - Title
TITLE = slice(0x134, 0x13F)

# 013F-0142 - Manufacturer Code
CODE = slice(0x13F, 0x143)

# 0143 - CGB Flag
CBG_FLAG = 0x143

# 0144-0145 - New Licensee Code
LICENSE = slice(0x144, 0x146)

# 0146 - SGB Flag
SBG_FLAG = 0x146

# 0147 - Cartridge Type
TYPE = 0x147

# 0148 - ROM Size
ROM_SIZE = 0x148

# 0149 - RAM Size
RAM_SIZE = 0x149

# 014A - Destination Code
DEST_CODE = 0x14A

# 014B - Old Licensee Code
OLD_LICENSE = 0x14B

# 014C - Mask ROM Version number
VERSION = 0x14C

# 014D - Header Checksum
HEADER_CHECKSUM = 0x14D

# 014E-014F - Global Checksum
GLOBAL_CHECKSUM = slice(0x14E, 0x150)

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
