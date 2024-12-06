from typing import Callable, TypeAlias


Point: TypeAlias = tuple[int, int]


def get_dimensions(matrix: list[list]):
    # assume no jagged arrays
    width = len(matrix[0])
    height = len(matrix)

    return width, height


def is_out_of_bounds(matrix: list[list], point: Point):
    width, height = get_dimensions(matrix)

    x, y = point[0], point[1]
    if x < 0 or x > width - 1:
        return True

    if y < 0 or y > height - 1:
        return True

    return False


def find[T](matrix: list[list[T]], predicate: Callable[[T], bool]) -> Point | None:
    width, height = get_dimensions(matrix)

    for y in range(height):
        for x in range(width):
            if predicate(matrix[y][x]):
                return (x, y)

    return None


def count[T](matrix: list[list[T]], predicate: Callable[[T], bool]) -> int:
    width, height = get_dimensions(matrix)

    count = 0
    for y in range(height):
        for x in range(width):
            if predicate(matrix[y][x]):
                count += 1

    return count


def apply_offset(position: Point, offset: tuple[int, int]):
    return (position[0] + offset[0], position[1] + offset[1])


def _walk_matrix[T](matrix: list[list[T]], x: int, y: int, distance: int, xdiff: int, ydiff: int):
    # we include the current cell in the distance
    distance = distance - 1

    width, height = get_dimensions(matrix)

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

    width, height = get_dimensions(matrix)

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
