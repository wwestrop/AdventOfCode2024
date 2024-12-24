from collections import defaultdict
from copy import deepcopy
from itertools import pairwise
from typing import Iterable
from util.types.matrix import Matrix
from util.types.point import Point
from util.driver import run


LEFT = Point(-1, 0)
UP = Point(0, -1)
RIGHT = Point(1, 0)
DOWN = Point(0, 1)


DIRECTIONS = [
    LEFT,
    UP,
    RIGHT,
    DOWN,
]


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
        if matrix[candidate_point]:
            edges[point].add(candidate_point)


def _build_graph(matrix: Matrix[bool]):
    edges: defaultdict[Point, set[Point]] = defaultdict(set)

    for y in range(matrix.height()):
        for x in range(matrix.width()):
            if matrix[Point(x, y)]:
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
        curr_node_dist = dist_from_start[curr_node]

        for neighbour in directed_graph[curr_node]:
            if neighbour in unvisited:
                dist_from_start[neighbour] = min(dist_from_start[neighbour], curr_node_dist + 1)

        unvisited.remove(curr_node)

    return dist_from_start


def _get_possible_cheats(maze: Matrix[bool]) -> Iterable[tuple[Point, Point, Point]]:
    for y in range(maze.height()):
        for x in range(maze.width()):
            p = Point(x, y)
            if maze[p]:
                for dir in DIRECTIONS:
                    w = list(maze.walk_up_to(p, dir, 3))
                    if [maze[o] for o in w] == [True, False, True]:
                        yield w


def _build_amended_graph(
    graph: defaultdict[Point, set[Point]],
    amended_cheat_edges: tuple[Point, Point, Point],
):
    new: defaultdict[Point, set[Point]] = deepcopy(graph)
    for e in pairwise(amended_cheat_edges):
        new[e[0]].add(e[1])

    return new


def part_1(lines: Iterable[str]):
    raw_cells = Matrix([[x for x in y] for y in lines])

    start_point = [c[0] for c in raw_cells.find(lambda p, s: s == "S")][0]
    end_point = [c[0] for c in raw_cells.find(lambda p, s: s == "E")][0]

    passable_cells: Matrix = raw_cells.transform(lambda p, s: s != "#")

    basic_maze = _build_graph(passable_cells)
    basic_cost = _shortest_paths(basic_maze, start_point)[end_point]

    cost_diffs: list[int] = []
    possible_cheats = _get_possible_cheats(passable_cells)

    i = 0
    possible_cheats = list(possible_cheats)

    for c in possible_cheats:
        amended = _build_amended_graph(basic_maze, c)
        cost = _shortest_paths(amended, start_point)[end_point]
        if basic_cost - cost >= 100:
            cost_diffs.append(basic_cost - cost)

        i += 1
        print(f"Tried cheat {i} / {len(possible_cheats)}")

    return len(cost_diffs)


run(20, part_1)
