from collections import defaultdict
from typing import Iterable
from util.types.matrix import Matrix
from util.parser import get_points
from util.types.point import Point
from util.driver import run

LEFT = Point(-1, 0)
UP = Point(0, -1)
RIGHT = Point(1, 0)
DOWN = Point(0, 1)


def _discover_connections(
    matrix: Matrix,
    edges: defaultdict[Point, set[Point]],
    point: Point,
):
    _add_edge_if_necessary(matrix, edges, point, UP)
    _add_edge_if_necessary(matrix, edges, point, DOWN)
    _add_edge_if_necessary(matrix, edges, point, LEFT)
    _add_edge_if_necessary(matrix, edges, point, RIGHT)


def _add_edge_if_necessary(
    matrix: Matrix,
    edges: defaultdict[Point, set[Point]],
    point: Point,
    offset: Point,
):
    candidate_point = point + offset
    if not matrix.is_out_of_bounds(candidate_point):
        if not matrix[candidate_point]:
            edges[point].add(candidate_point)


def _build_graph(matrix: Matrix):
    edges: defaultdict[Point, set[Point]] = defaultdict(set)

    for y in range(matrix.height()):
        for x in range(matrix.width()):
            _discover_connections(matrix, edges, Point(x, y))

    return edges


def _find_shortest_unvisited(costs: dict[Point, int], unvisited: set[Point]):
    shortest_found: tuple[Point, int] = (None, 999999999999)
    for v in costs:
        if v in unvisited:
            if costs[v] < shortest_found[1]:
                shortest_found = (v, costs[v])

    return shortest_found[0]


def _shortest_paths(directed_graph: defaultdict[Point, set[Point]], start: Point) -> dict[Point, int]:
    unvisited = set(directed_graph.keys())

    dist_from_start = defaultdict[Point, int](lambda: 999999999999)
    dist_from_start[start] = 0

    while any(unvisited):
        curr_node = _find_shortest_unvisited(dist_from_start, unvisited)
        if curr_node is None:
            # not reachable
            break
        curr_node_dist = dist_from_start[curr_node]

        for neighbour in directed_graph[curr_node]:
            if neighbour in unvisited:
                dist_from_start[neighbour] = min(dist_from_start[neighbour], curr_node_dist + 1)

        unvisited.remove(curr_node)

    return dist_from_start


def _corrupt_memory(corrupt_grid: Matrix, points: Iterable[Point]):
    for p in list(points):
        corrupt_grid[p] = True


def part_1(corruptions: Iterable[Point]):
    max = 70
    corrupt_grid = Matrix([[False for x in range(max + 1)] for y in range(max + 1)])
    _corrupt_memory(corrupt_grid, list(corruptions)[:1024])

    start = Point(0, 0)
    end = Point(max, max)

    graph = _build_graph(corrupt_grid)
    shortest_paths = _shortest_paths(graph, start)
    return shortest_paths[end]


def _binary_search(
    start: Point,
    end: Point,
    corruptions: list[Point],
):
    grid_max = 70

    start = Point(0, 0)
    end = Point(grid_max, grid_max)

    min = 0
    max = len(corruptions)

    while True:
        attempt = (max - min) / 2 + min  # TODO what if this causes rounding
        # assert floor(attempt) == attempt
        attempt = int(attempt)

        print(f"{min} < n < {max} : ", end="")
        print(f"Trying {attempt} bytes (last={corruptions[:attempt][-1]}) -> ", end="")
        corrupt_grid = Matrix([[False for x in range(grid_max + 1)] for y in range(grid_max + 1)])
        _corrupt_memory(corrupt_grid, corruptions[:attempt])
        graph = _build_graph(corrupt_grid)

        shortest_paths = _shortest_paths(graph, start)
        if shortest_paths[end] == 999999999999:
            max = attempt
            print("unreachable")
        else:
            min = attempt
            print(f"reachable in {shortest_paths[end]}")

        # print(corrupt_grid.transform(lambda p, s: "#" if s else "."))

        if abs(max - min) < 2:
            return corruptions[max]


def part_2(corruptions: Iterable[Point]):
    max = 70

    start = Point(0, 0)
    end = Point(max, max)

    return _binary_search(start, end, list(corruptions))


run(18, part_2, parser=get_points)
