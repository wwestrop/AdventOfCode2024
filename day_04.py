from typing import Iterable

from util import run, walk_compass_directions


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


run(4, find_xmas, parser=lambda l: list(l))
