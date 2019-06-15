from enum import IntEnum


__all__ = [
    "Shelf",
]


class Shelf(IntEnum):
    TOREAD = 1
    READING = 2
    READ = 3
    OWNED = 3
