from dataclasses import dataclass
from typing import Iterable, TypeAlias

from util.matrix import apply_offset, count, find, is_out_of_bounds
from util.driver import run


Point: TypeAlias = tuple[int, int]


@dataclass(frozen=True)
class Direction:
    offset: tuple[int, int]


UP = Direction(offset=(0, -1))
RIGHT = Direction(offset=(1, 0))
DOWN = Direction(offset=(0, 1))
LEFT = Direction(offset=(-1, 0))

ROT_90 = {
    UP: RIGHT,
    RIGHT: DOWN,
    DOWN: LEFT,
    LEFT: UP,
}


def _get_direction(char):
    match char:
        case "^":
            return UP
        case ">":
            return RIGHT
        case "v":
            return DOWN
        case "<":
            return LEFT


def part_1(lines: Iterable[str]):
    raw_map = [[cell for cell in line] for line in lines]

    position = find(raw_map, lambda c: c in ["^", ">", "v", "<"])
    if not position:
        raise "shouldnt happen for the examples i'm given, but generic find method might be used where it could"

    obstacle_map = [[cell == "#" for cell in line] for line in raw_map]
    visited = [[False for cell in line] for line in raw_map]
    visited[position[1]][position[0]] = True
    direction = _get_direction(raw_map[position[1]][position[0]])
    if not direction:
        raise "shouldnt happen for the examples i'm given"

    while True:
        cell_in_front = apply_offset(position, direction.offset)
        if is_out_of_bounds(obstacle_map, cell_in_front):
            return count(visited, lambda c: c is True)

        if obstacle_map[cell_in_front[1]][cell_in_front[0]]:
            direction = ROT_90[direction]
        else:
            position = cell_in_front
            visited[cell_in_front[1]][cell_in_front[0]] = True


run(6, part_1)
