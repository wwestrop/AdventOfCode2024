from typing import Iterable
from util.types.matrix import Matrix
from util.types.point import Point
from util.driver import run


SPACE = "."
BOX = "O"
WALL = "#"
ROBOT = "@"

DIRECTIONS = {
    "^": Point(0, -1),
    ">": Point(1, 0),
    "v": Point(0, 1),
    "<": Point(-1, 0),
}


def _parse(lines: Iterable[str]):
    lines = list(lines)
    map_lines = []
    movement_lines = []

    for i in range(len(lines)):
        if lines[i].strip() == "":
            map_lines = lines[:i]
            movement_lines = lines[i + 1 :]

    grid = Matrix[str]([[c for c in line] for line in map_lines])
    movement_lines = "".join(movement_lines)
    return grid, [DIRECTIONS[m] for m in movement_lines]


def _calculate_box_score(grid: Matrix[str]):
    points = [f[0] for f in grid.find(lambda p, c: c == BOX)]

    score = 0
    for p in points:
        score += p.y * 100 + p.x

    return score


def part_1(lines: Iterable[str]):
    grid, movements = _parse(lines)

    robot = [r[0] for r in grid.find(lambda p, s: s == ROBOT)][0]

    for m in movements:
        new_position = robot + m
        if grid.is_out_of_bounds(new_position):
            assert False, "Can this ever happen?"
        elif grid[new_position] == SPACE:
            grid[robot] = SPACE
            robot = new_position
            grid[robot] = ROBOT
        elif grid[new_position] == WALL:
            pass
        elif grid[new_position] == BOX:
            for c in grid.walk_matrix(robot, m):
                if grid[c] == WALL:
                    break
                if grid[c] == SPACE:
                    grid[c] = BOX
                    grid[robot] = SPACE
                    robot = new_position
                    grid[robot] = ROBOT
                    break

    return _calculate_box_score(grid)


run(15, part_1)
