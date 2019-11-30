"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""


class EmulationError(Exception):
    """The emulation has encountered a fatal error."""


class InvalidRom(EmulationError):
    """The ROM has an invalid header checksum."""

    def __init__(self, error: str):
        self.error = error
        super().__init__(error)

    def __repr__(self):
        return f"{type(self).__name__}: {self.error}."

    def __str__(self):
        return repr(self)


class InvalidZip(EmulationError):
    """The ZIP file contains no gameboy ROM."""

    def __repr__(self):
        return f"{type(self).__name__}: the ZIP file contains no gameboy ROM."

    def __str__(self):
        return repr(self)
