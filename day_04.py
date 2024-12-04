from typing import Iterable

from util import run, walk_compass_directions, walk_x_shape


def find_xmas(lines: Iterable[list[str]]):
    matrix = list(lines)

    # assume no jagged arrays
    width = len(matrix[0])
    height = len(matrix)

    SOUGHT_WORD = list("XMAS")

    count = 0

    for y in range(height):
        for x in range(width):
            for walked_path in walk_compass_directions(matrix, x, y, len(SOUGHT_WORD)):
                if walked_path == SOUGHT_WORD:
                    count += 1

    return count


def find_x_shaped_mas(lines: Iterable[list[str]]):
    matrix = list(lines)

    # assume no jagged arrays
    width = len(matrix[0])
    height = len(matrix)

    SOUGHT_WORD = list("MAS")
    BACKWARDS_SOUGHT_WORD = list(reversed("MAS"))

    count = 0

    for y in range(height):
        for x in range(width):
            x_bars = list(walk_x_shape(matrix, x, y, len(SOUGHT_WORD)))
            if (
                len(x_bars) == 2
                and (x_bars[0] == SOUGHT_WORD or x_bars[0] == BACKWARDS_SOUGHT_WORD)
                and (x_bars[1] == SOUGHT_WORD or x_bars[1] == BACKWARDS_SOUGHT_WORD)
            ):
                count += 1

    return count


run(4, find_xmas, find_x_shaped_mas, parser=lambda l: list(l))
