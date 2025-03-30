"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy.
"""

from pathlib import Path

import pytest

from gameboy.__main__ import main, usage


def test_usage() -> None:
    """Test the `usage()` return code."""
    assert usage() == -1


def test_invalid_action(mario: Path) -> None:
    """Test the ROM 'check' argument."""
    with pytest.raises(ValueError, match="Invalid action ='boom'"):
        main(mario, "boom")


def test_check(mario: Path) -> None:
    """Test the ROM 'check' argument."""
    assert main(mario, "check") == 0


def test_check_bad(roms: Path) -> None:
    """Test the ROM 'check' argument whith a bad ROM file."""
    assert main(roms / "invalid.gb", "check") == 1


def test_dump(mario: Path) -> None:
    """Test the ROM 'dump' argument."""
    assert main(mario, "dump") == 0
