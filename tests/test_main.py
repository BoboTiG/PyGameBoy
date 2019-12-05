"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from gameboy.__main__ import main


def test_no_args():
    """Test with zero argument."""
    assert main() == 1


def test_no_action(mario):
    """Test with a ROM but no action."""
    assert main(mario) == 0


def test_check(mario):
    """Test the ROM 'check' argument'."""
    assert main(mario, "check") == 0


def test_check_bad(roms):
    """Test the ROM 'check' argument whith a bad ROM file."""
    assert main(roms / "invalid.gb", "check") == 1


def test_dump(mario):
    """Test the ROM 'dump' argument."""
    assert main(mario, "dump") == 0
