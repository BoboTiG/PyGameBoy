"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from functools import cached_property, lru_cache
from pathlib import Path
from types import SimpleNamespace
from typing import Union
from zipfile import ZipFile

from . import constants, offset
from .exceptions import InvalidRomError, InvalidZipError


# The type of data that Cartridge.__init__() can handle as a "ROM"
InputData = Union[Path, bytes, str]


class Cartridge:
    """Cartridge content."""

    def __init__(self, rom: InputData) -> None:
        """*rom* can be either bytes, a string or a path-like object."""

        if isinstance(rom, Path):
            self.rom = rom
        elif isinstance(rom, str):
            self.rom = Path(rom)
        else:
            self.rom = Path(".")

        if isinstance(rom, bytes):
            self.data = rom
        else:
            # Handle ZIP files: the first ROM file found is used
            if self.rom.suffix.lower() == ".zip":
                with ZipFile(self.rom) as zfile:
                    for file in zfile.namelist():
                        if file.lower().endswith((".gb", ".gbc")):
                            self.data = zfile.read(file)
                            break
                    else:
                        raise InvalidZipError()
            else:
                self.data = self.rom.read_bytes()

        if len(self.data) < 0x14E or not self.is_valid():
            raise InvalidRomError("the ROM has invalid headers")

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}<"
            f"name={self.rom.name!r}"
            f", title={self.title!r}"
            f", version={self.version!r}"
            f", destination={self.destination!r}"
            f", publisher={self.publisher!r}"
            f", color={self.cgb_flag!r}"
            f", valid={self.is_valid(complete=True)!r}"
            ">"
        )

    @lru_cache(maxsize=1)
    def parse(self) -> SimpleNamespace:
        """Retrieve all ROM information."""
        try:
            return SimpleNamespace(
                cgb=self.cgb_flag,
                code=self.code,
                destination=self.destination,
                file=self.rom,
                licensee=self.licensee,
                old_licensee=self.old_licensee,
                publisher=self.publisher,
                ram_size=self.ram_size,
                rom_size=self.rom_size,
                sgb=self.sgb_flag,
                title=self.title,
                type=self.type,
                valid=self.header_checksum,
                valid_complete=self.global_checksum,
                version=self.version,
            )
        except Exception:
            raise InvalidRomError("ROM parsing error")

    @cached_property
    def logo(self) -> bytes:
        """Nintendo Logo
        These bytes define the bitmap of the Nintendo logo that is displayed when the
        gameboy gets turned on. The hexdump of this bitmap is:
          CE ED 66 66 CC 0D 00 0B 03 73 00 83 00 0C 00 0D
          00 08 11 1F 88 89 00 0E DC CC 6E E6 DD DD D9 99
          BB BB 67 63 6E 0E EC CC DD DC 99 9F BB B9 33 3E
        The gameboys boot procedure verifies the content of this bitmap (after it has
        displayed it), and LOCKS ITSELF UP if these bytes are incorrect. A CGB
        verifies only the first 18h bytes of the bitmap, but others (for example a
        pocket gameboy) verify all 30h bytes.
        """
        return self.data[offset.LOGO]

    @cached_property
    def title(self) -> str:
        """Title
        Title of the game in UPPER CASE ASCII. If it is less than 16 characters then
        the remaining bytes are filled with 00's. When inventing the CGB, Nintendo has
        reduced the length of this area to 15 characters, and some months later they
        had the fantastic idea to reduce it to 11 characters only. The new meaning of
        the ex-title bytes is described below.
        """
        full_title = self.data[offset.TITLE].decode("latin-1").rstrip("\0")
        code = self.code
        if code:
            full_title += code
        return full_title

    @cached_property
    def code(self) -> str:
        """Manufacturer Code
        In older cartridges this area has been part of the Title (see above), in newer
        cartridges this area contains an 4 character uppercase manufacturer code.
        Purpose and Deeper Meaning unknown.
        """
        return self.data[offset.CODE].decode("latin-1").rstrip("\0")

    @cached_property
    def cgb_flag(self) -> bool:
        """CGB Flag
        In older cartridges this byte has been part of the Title (see above). In CGB
        cartridges the upper bit is used to enable CGB functions. This is required,
        otherwise the CGB switches itself into Non-CGB-Mode. Typical values are:
          80h - Game supports CGB functions, but works on old gameboys also.
          C0h - Game works on CGB only (physically the same as 80h).
        Values with Bit 7 set, and either Bit 2 or 3 set, will switch the gameboy into
        a special non-CGB-mode with uninitialized palettes. Purpose unknown,
        eventually this has been supposed to be used to colorize monochrome games that
        include fixed palette data at a special location in ROM.
        """
        return self.data[offset.CBG_FLAG] in (0x80, 0xC0)

    @cached_property
    def licensee(self) -> str:
        """New Licensee Code
        Specifies a two character ASCII licensee code, indicating the company or
        publisher of the game. These two bytes are used in newer games only (games
        that have been released after the SGB has been invented). Older games are
        using the header entry at 014B instead.
        """
        return self.data[offset.LICENSE].decode("latin-1").rstrip("\0")

    @cached_property
    def sgb_flag(self) -> bool:
        """SGB Flag
        Specifies whether the game supports SGB functions, common values are:
          00h = No SGB functions (Normal Gameboy or CGB only game)
          03h = Game supports SGB functions
        The SGB disables its SGB functions if this byte is set to another value than
        03h.
        """
        return self.data[offset.SBG_FLAG] == 0x03

    @cached_property
    def type(self) -> str:
        """Cartridge Type
        Specifies which Memory Bank Controller (if any) is used in the cartridge, and
        if further external hardware exists in the cartridge.
          00h  ROM ONLY                 13h  MBC3+RAM+BATTERY
          01h  MBC1                     15h  MBC4
          02h  MBC1+RAM                 16h  MBC4+RAM
          03h  MBC1+RAM+BATTERY         17h  MBC4+RAM+BATTERY
          05h  MBC2                     19h  MBC5
          06h  MBC2+BATTERY             1Ah  MBC5+RAM
          08h  ROM+RAM                  1Bh  MBC5+RAM+BATTERY
          09h  ROM+RAM+BATTERY          1Ch  MBC5+RUMBLE
          0Bh  MMM01                    1Dh  MBC5+RUMBLE+RAM
          0Ch  MMM01+RAM                1Eh  MBC5+RUMBLE+RAM+BATTERY
          0Dh  MMM01+RAM+BATTERY        FCh  POCKET CAMERA
          0Fh  MBC3+TIMER+BATTERY       FDh  BANDAI TAMA5
          10h  MBC3+TIMER+RAM+BATTERY   FEh  HuC3
          11h  MBC3                     FFh  HuC1+RAM+BATTERY
          12h  MBC3+RAM
        """
        return constants.TYPES[self.data[offset.TYPE]]

    @cached_property
    def rom_size(self) -> str:
        """ROM Size
        Specifies the ROM Size of the cartridge. Typically calculated as "32KB shl N".
          00h -  32KByte (no ROM banking)
          01h -  64KByte (4 banks)
          02h - 128KByte (8 banks)
          03h - 256KByte (16 banks)
          04h - 512KByte (32 banks)
          05h -   1MByte (64 banks)  - only 63 banks used by MBC1
          06h -   2MByte (128 banks) - only 125 banks used by MBC1
          07h -   4MByte (256 banks)
          52h - 1.1MByte (72 banks)
          53h - 1.2MByte (80 banks)
          54h - 1.5MByte (96 banks)
        """
        return constants.ROM_SIZES[self.data[offset.ROM_SIZE]]

    @cached_property
    def ram_size(self) -> str:
        """RAM Size
        Specifies the size of the external RAM in the cartridge (if any).
          00h - None
          01h - 2 KBytes
          02h - 8 Kbytes
          03h - 32 KBytes (4 banks of 8KBytes each)
        When using a MBC2 chip 00h must be specified in this entry, even though the
        MBC2 includes a built-in RAM of 512 x 4 bits.
        """
        return constants.RAM_SIZES[self.data[offset.RAM_SIZE]]

    @cached_property
    def destination(self) -> str:
        """Destination Code
        Specifies if this version of the game is supposed to be sold in japan, or
        anywhere else. Only two values are defined.
          00h - Japanese
          01h - Non-Japanese
        """
        return "Japan" if self.data[offset.DEST_CODE] == 0x00 else "World"

    @cached_property
    def old_licensee(self) -> str:
        """Old Licensee Code
        Specifies the games company/publisher code in range 00-FFh. A value of 33h
        signalizes that the New License Code in header bytes 0144-0145 is used
        instead.
        (Super GameBoy functions won't work if <> $33.)
        """
        value = self.data[offset.OLD_LICENSE]
        if value == 0x33:
            # Then .licensee will be used by .publisher
            return ""
        return f"{value:02X}"

    @cached_property
    def version(self) -> float:
        """Mask ROM Version number
        Specifies the version number of the game. That is usually 00h.
        """
        return 1.0 + (self.data[offset.VERSION] / 10)

    @cached_property
    def header_checksum(self) -> bool:
        """Header Checksum
        Contains an 8 bit checksum across the cartridge header bytes 0134-014C. The
        checksum is calculated as follows:
          x=0:FOR i=0134h TO 014Ch:x=x-MEM[i]-1:NEXT
        The lower 8 bits of the result must be the same than the value in this entry.
        The GAME WON'T WORK if this checksum is incorrect.
        """
        checksum = 0
        for value in self.data[offset.TITLE.start : offset.HEADER_CHECKSUM]:
            checksum = checksum - value - 1
        checksum &= 0xFF
        return checksum == self.data[offset.HEADER_CHECKSUM]

    @cached_property
    def global_checksum(self) -> bool:
        """Global Checksum
        Contains a 16 bit checksum (upper byte first) across the whole cartridge ROM.
        Produced by adding all bytes of the cartridge (except for the two checksum
        bytes) modulo 2**16 in big endian format. The Gameboy doesn't verify this checksum.
        """
        low, high = self.data[offset.GLOBAL_CHECKSUM]
        awaited = (low << 8) | high
        checksum = sum(self.data) - low - high
        checksum %= 2 ** 16
        return checksum == awaited

    @cached_property
    def publisher(self) -> str:
        """Convenient property to get the ROM publisher."""
        licensee = self.old_licensee or self.licensee
        return constants.LICENSEES[licensee]

    def is_valid(self, complete: bool = False) -> bool:
        """Verify the header validity."""
        if self.header_checksum is False:
            return False
        if complete:
            return self.global_checksum is True
        return True
