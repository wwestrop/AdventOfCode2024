from typing import Iterable
from util.driver import run


def _get_type(lines: list[str]):
    if all(l == "#" for l in lines[0]):
        return "LOCK"
    else:
        return "KEY"


def _get_heights(lines: list[str]):
    """
    The height is assumed to be of the lock pins. If a key, invert them
    """
    heights: list[int] = []

    for x in range(len(lines[0])):
        for y in range(len(lines)):
            if lines[y][x] != "#":
                heights.append(y - 1)
                break

    return heights


def _key_would_foul_pins(key: list[int], lock: list[int]):
    # Took a shortcut, my inputs are always 7 rows tall (of which, the top and bottom rows are always solid for a key-lock pair)
    HEIGHT = 5
    for x in range(len(key)):
        if key[x] + lock[x] > HEIGHT:
            print(f"Lock {lock} with key {key} -> OVERLAP in column {x + 1}")
            return True

    print(f"Lock {lock} with key {key} -> all columns fit!")
    return False


def _parse_schematics(lines: Iterable[str]):
    acc = []
    for line in lines:
        if line.strip() == "":
            yield acc
            acc = []
        else:
            acc.append(line)

    if acc != []:
        yield acc


def _parse(lines: Iterable[str]):
    schematics = _parse_schematics(lines)

    locks: list[list[int]] = []
    keys: list[list[int]] = []

    for s in schematics:
        if _get_type(s) == "LOCK":
            locks.append(_get_heights(s))
        else:
            keys.append(_get_heights(list(reversed(s))))

    return locks, keys


def part_1(lines: Iterable[str]):
    locks, keys = _parse(lines)

    count = 0
    for lock in locks:
        for key in keys:
            if not _key_would_foul_pins(key, lock):
                count += 1

    return count


run(25, part_1)
