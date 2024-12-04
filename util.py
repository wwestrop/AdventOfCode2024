import os
from typing import Callable, Iterable


def _no_op(input):
    return input


def _get_input[T](filename: str, parser: Callable[[str], T]) -> Iterable[T]:
    with open(filename) as file:
        line = ""

        while True:
            line = file.readline()
            line = line.replace("\r", "").replace("\n", "")

            if line != "":
                yield parser(line)
            else:
                return


def get_int_list(line: str):
    return [int(v) for v in line.split(" ") if v != ""]


def get_int_pairs(line: str):
    line_values = [v for v in line.split(" ") if v != ""]

    return int(line_values[0]), int(line_values[1])


def _run_for_file[TIn, TOut](filename: str, runner: Callable[[Iterable[TIn]], TOut], parser: Callable[[str], TIn]):
    input_data = _get_input(filename, parser) if os.path.isfile(filename) else None
    result = runner(input_data) if input_data is not None else "[X]"

    print(f"{filename.ljust(28) } -> {result}")


def _run_for[TIn, TOut](day: int, runner: Callable[[Iterable[TIn]], TOut], parser: Callable[[str], TIn]):
    day_num = str(day).rjust(2, "0")
    example_filename = f"inputs/day{day_num}-example.txt"
    input_filename = f"inputs/day{day_num}.txt"

    _run_for_file(example_filename, runner, parser)
    _run_for_file(input_filename, runner, parser)


def run[TIn, TOut](
    day: int,
    runner1: Callable[[Iterable[TIn]], TOut],
    runner2: Callable[[Iterable[TIn]], TOut] | None = None,
    parser: Callable[[str], TIn] = _no_op,
):
    _run_for(day, runner1, parser)

    if runner2 is not None:
        print("--------------------------------------------------")
        _run_for(day, runner2, parser)


def remove_at[T](input: list[T], i: int) -> list[T]:
    copy = list(input)
    del copy[i]

    return copy


def _walk_matrix[T](matrix: list[list[T]], x: int, y: int, distance: int, xdiff: int, ydiff: int):
    # we include the current cell in the distance
    distance = distance - 1

    # assume no jagged arrays
    width = len(matrix[0])
    height = len(matrix)

    if x + xdiff * distance < 0 or x + xdiff * distance >= width:
        return

    if y + ydiff * distance < 0 or y + ydiff * distance >= height:
        return

    path = []
    for i in range(distance + 1):
        path.append(matrix[y][x])  # note - x&y inverted

        x += xdiff
        y += ydiff

    return path


def walk_x_shape[T](matrix: list[list[T]], x: int, y: int, distance: int):
    """
    Walks an X-shape of length `distance`, centered on (x,y)
    """

    # assume no jagged arrays
    width = len(matrix[0])
    height = len(matrix)

    offset = int((distance - 1) / 2)

    if x - offset < 0 or x + offset >= width:
        return

    if y - offset < 0 or y + offset >= height:
        return

    # /
    yield _walk_matrix(matrix, x - offset, y + offset, distance, xdiff=1, ydiff=-1)

    # \
    yield _walk_matrix(matrix, x - offset, y - offset, distance, xdiff=1, ydiff=1)


def walk_compass_directions[T](matrix: list[list[T]], x: int, y: int, distance: int):
    """
    Starting at the point (x,y), walk the specified distance in each of the
    compass directions, and return arrays of each of the elements walked through.

    If there is not enough space to walk in a given direction, then that
    direction will not be walked at all
    """

    # North
    yield _walk_matrix(matrix, x, y, distance, xdiff=0, ydiff=-1)

    # North East
    yield _walk_matrix(matrix, x, y, distance, xdiff=1, ydiff=-1)

    # East
    yield _walk_matrix(matrix, x, y, distance, xdiff=1, ydiff=0)

    # South East
    yield _walk_matrix(matrix, x, y, distance, xdiff=1, ydiff=1)

    # South
    yield _walk_matrix(matrix, x, y, distance, xdiff=0, ydiff=1)

    # South West
    yield _walk_matrix(matrix, x, y, distance, xdiff=-1, ydiff=1)

    # West
    yield _walk_matrix(matrix, x, y, distance, xdiff=-1, ydiff=0)

    # North West
    yield _walk_matrix(matrix, x, y, distance, xdiff=-1, ydiff=-1)
