from typing import Iterable
from util.types.matrix import Matrix
from util.types.point import Point
from util.driver import run


def _find_adjacent_cells[T](matrix: Matrix[T], start_point: Point, visited: set[Point] = None) -> set[Point]:
    visited = set() if visited == None else visited

    result = set()

    result.add(start_point)
    visited.add(start_point)

    for d in matrix.x_y_adjacent(start_point):
        if d in visited:
            continue
        elif matrix[d] == matrix[start_point]:
            result = result.union(_find_adjacent_cells(matrix, d, visited))

    return result


def _calculate_perimeter(matrix: Matrix[str], cells: set[Point]):
    perimeter = 0

    for cell in cells:
        perimeter += 4
        for neighbour in matrix.x_y_adjacent(cell):
            if matrix[neighbour] == matrix[cell]:
                perimeter -= 1

    return perimeter


def _find_regions(matrix: Matrix[str]):
    all_points = set(matrix.visit(lambda p, _: p))
    while any(all_points):
        p = all_points.pop()
        region = _find_adjacent_cells(matrix, p)

        all_points = all_points - region

        yield region


def part_1(lines: Iterable[list[str]]):
    plots = Matrix(list(lines))

    cost = 0
    for region in _find_regions(plots):
        area = len(region)
        perim = _calculate_perimeter(plots, region)
        cost += area * perim

    return cost


run(12, part_1, parser=lambda line: [c for c in line])
