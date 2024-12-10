from typing import Iterable
from util.types.point import Point
from util.types.matrix import Matrix
from util.driver import run


LEFT = Point(-1, 0)
UP = Point(0, -1)
RIGHT = Point(1, 0)
DOWN = Point(0, 1)


def _discover_connections(
    matrix: Matrix[int],
    edges: dict[Point, set[Point]],
    point: Point,
):
    _add_edge_if_necessary(matrix, edges, point, UP)
    _add_edge_if_necessary(matrix, edges, point, DOWN)
    _add_edge_if_necessary(matrix, edges, point, LEFT)
    _add_edge_if_necessary(matrix, edges, point, RIGHT)


def _add_edge_if_necessary(
    matrix: Matrix[int],
    edges: dict[Point, set[Point]],
    point: Point,
    offset: Point,
):
    candidate_point = point + offset
    if not matrix.is_out_of_bounds(candidate_point):
        if matrix[candidate_point] - matrix[point] == 1:
            if point not in edges:
                edges[point] = set()

            edges[point].add(candidate_point)


def _build_graph(matrix: Matrix[int]):
    edges: dict[Point, set[Point]] = dict()

    for y in range(matrix.height()):
        for x in range(matrix.width()):
            _discover_connections(matrix, edges, Point(x, y))

    return edges


def _can_walk(edges: dict[Point, set[Point]], start: Point, end: Point, current_path_len=0) -> bool:
    if start == end:
        return True

    if current_path_len > 9:
        return False

    out_vertices = edges[start] if start in edges else []
    for v in out_vertices:
        if _can_walk(edges, v, end, current_path_len + 1):
            return True

    return False


def part_1(lines: Iterable[list[int]]):
    map = Matrix(list(lines))

    trail_starts = [p for p, h in map.visit(lambda p, h: (p, h)) if h == 0]
    trail_ends = [p for p, h in map.visit(lambda p, h: (p, h)) if h == 9]

    graph = _build_graph(map)

    count_routes = 0

    for s in trail_starts:
        for e in trail_ends:
            if _can_walk(graph, s, e):
                count_routes += 1

    return count_routes


run(10, part_1, parser=lambda line: [int(c) for c in line])
