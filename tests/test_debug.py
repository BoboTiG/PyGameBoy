"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""

from gameboy.debug import hexdump


def test_hexdump():
    data = (b'\xce\xedff\xcc\r\x00\x0b\x03s\x00\x83\x00\x0c\x00\r\x00\x08\x11'
            b'\x1f\x88\x89\x00\x0e\xdc\xccn\xe6\xdd\xdd\xd9\x99\xbb\xbbgcn\x0e'
            b'\xec\xcc\xdd\xdc\x99\x9f\xbb\xb93>')
    result = ('CE ED 66 66 CC 0D 00 0B 03 73 00 83 00 0C 00 0D\n'
              '00 08 11 1F 88 89 00 0E DC CC 6E E6 DD DD D9 99\n'
              'BB BB 67 63 6E 0E EC CC DD DC 99 9F BB B9 33 3E')
    assert hexdump(data) == result
