"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy.
"""


class EmulationError(Exception):
    """The emulation has encountered a fatal error."""


class InvalidRomError(EmulationError):
    """The ROM has an invalid header checksum."""

    def __init__(self, error: str) -> None:
        self.error = error
        super().__init__(error)

    def __repr__(self) -> str:
        return f"{type(self).__name__}: {self.error}."

    def __str__(self) -> str:
        return repr(self)


class InvalidZipError(EmulationError):
    """The ZIP file contains no gameboy ROM."""

    def __repr__(self) -> str:
        return f"{type(self).__name__}: the ZIP file contains no gameboy ROM."

    def __str__(self) -> str:
        return repr(self)
