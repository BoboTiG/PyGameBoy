"""This is part of PyGameBoy, a Game Boy emulator written in Python 3.
Source: https://github.com/BoboTiG/PyGameBoy
"""


class Swap:
    """Context manager to swap an attribute's value:

        >>> # self.person equals 'Alice'
        >>> with Swap(self, 'person', 'Bob'):
        ...     # ...
    """

    def __init__(self, obj, attr, value):
        self.obj = obj
        self.attr = attr
        self.value = value
        self.old_value = getattr(obj, attr)

    def __enter__(self):
        setattr(self.obj, self.attr, self.value)

    def __exit__(self, *args):
        setattr(self.obj, self.attr, self.old_value)
