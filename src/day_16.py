from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

from util.types.matrix import Matrix
from util.types.point import Point
from util.driver import run


type graph = defaultdict[Vertex, list[Edge]]


UP = Point(0, -1)
RIGHT = Point(1, 0)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)

ROT_90 = {
    UP: RIGHT,
    RIGHT: DOWN,
    DOWN: LEFT,
    LEFT: UP,
}


@dataclass(frozen=True)
class Vertex:
    point: Point
    direction: Point

    def __repr__(self):
        direction = (
            "UP"
            if self.direction == UP
            else "RIGHT"
            if self.direction == RIGHT
            else "DOWN"
            if self.direction == DOWN
            else "LEFT"
        )

        return f"({self.point.x},{self.point.y}) {direction}"


@dataclass(frozen=True)
class Edge:
    src: Vertex
    dst: Vertex
    cost: int

    def __repr__(self):
        src_dir = (
            "UP"
            if self.src.direction == UP
            else "RIGHT"
            if self.src.direction == RIGHT
            else "DOWN"
            if self.src.direction == DOWN
            else "LEFT"
        )
        dst_dir = (
            "UP"
            if self.dst.direction == UP
            else "RIGHT"
            if self.dst.direction == RIGHT
            else "DOWN"
            if self.dst.direction == DOWN
            else "LEFT"
        )
        return f"{src_dir}({self.src.point.x},{self.src.point.y}) -> {dst_dir}({self.dst.point.x},{self.dst.point.y})  {{{self.cost}}}"


def _build_cell_vertices(
    cell: Point,
    directed_graph: defaultdict[Vertex, list[Edge]],
):
    cell_vertex_n = Vertex(point=cell, direction=UP)
    cell_vertex_e = Vertex(point=cell, direction=RIGHT)
    cell_vertex_s = Vertex(point=cell, direction=DOWN)
    cell_vertex_w = Vertex(point=cell, direction=LEFT)

    cell_edges = [
        Edge(src=cell_vertex_n, dst=cell_vertex_e, cost=1000),
        Edge(src=cell_vertex_e, dst=cell_vertex_s, cost=1000),
        Edge(src=cell_vertex_s, dst=cell_vertex_w, cost=1000),
        Edge(src=cell_vertex_w, dst=cell_vertex_n, cost=1000),
        Edge(src=cell_vertex_n, dst=cell_vertex_w, cost=1000),
        Edge(src=cell_vertex_w, dst=cell_vertex_s, cost=1000),
        Edge(src=cell_vertex_s, dst=cell_vertex_e, cost=1000),
        Edge(src=cell_vertex_e, dst=cell_vertex_n, cost=1000),
    ]

    for e in cell_edges:
        directed_graph[e.src].append(e)

    return [
        cell_vertex_n,
        cell_vertex_e,
        cell_vertex_s,
        cell_vertex_w,
    ]


def _build_cell_vertex_quads(
    maze: Matrix[str],
    directed_graph: graph,
):
    """
    Each cell is represented as a vertex quad, one for each compass direction, with an expesive edge to rotate 90° between them.
    Cheaper edges to walk between quads (in the direction of that part of the quad) are added later
    """
    unvisited = {p for p, s in maze.find(lambda p, s: s != "#")}

    while any(unvisited):
        cell = unvisited.pop()

        if maze.is_out_of_bounds(cell):
            continue

        if maze[cell] == "#":
            continue

        _build_cell_vertices(cell, directed_graph)


def _build_point_vertex_lookup(directed_graph: graph):
    point_vertex_lookup: defaultdict[Point, list[Vertex]] = defaultdict(list)
    for vertex in directed_graph:
        point_vertex_lookup[vertex.point].append(vertex)

    return point_vertex_lookup


def _get_linkable_vertex(cell: Point, vertex: Vertex, point_vertex_lookup: defaultdict[Point, list[Vertex]]):
    cell_to_link = vertex.point + vertex.direction

    if cell_to_link not in point_vertex_lookup:
        return None

    # find the one vertex in the cell in that direction which is going same direction as this vertex
    return [v for v in point_vertex_lookup[cell_to_link] if v.direction == vertex.direction][0]


def _connect_cells(maze: Matrix[str], cell: Point, unvisited: set[Point], directed_graph: graph):
    point_vertex_lookup = _build_point_vertex_lookup(directed_graph)

    if maze.is_out_of_bounds(cell):
        return

    if maze[cell] == "#":
        return

    if cell not in unvisited:
        return

    unvisited.remove(cell)

    all_vertices = directed_graph.keys()
    for vertex in all_vertices:
        linker = _get_linkable_vertex(cell, vertex, point_vertex_lookup)
        if linker:
            directed_graph[vertex].append(Edge(src=vertex, dst=linker, cost=1))


def _find_shortest_unvisited(costs: dict[Vertex, int], unvisited: set[Vertex]):
    shortest_found: tuple[Vertex, int] = (None, 999999999999)
    for v in costs:
        if v in unvisited:
            if costs[v] < shortest_found[1]:
                shortest_found = (v, costs[v])

    return shortest_found[0]


def _shortest_paths(directed_graph: defaultdict[Vertex, list[Edge]], start: Vertex) -> dict[Vertex, int]:
    unvisited = set(directed_graph.keys())

    dist_from_start = defaultdict[Vertex, int](lambda: 999999999999)
    dist_from_start[start] = 0

    while any(unvisited):
        curr_node = _find_shortest_unvisited(dist_from_start, unvisited)
        curr_node_dist = dist_from_start[curr_node]

        for edge in directed_graph[curr_node]:
            if edge.dst in unvisited:
                dist_from_start[edge.dst] = min(dist_from_start[edge.dst], curr_node_dist + edge.cost)

        unvisited.remove(curr_node)
        if len(unvisited) % 100 == 0:
            print(f"Visited {len(directed_graph) - len(unvisited)} / {len(directed_graph)}")

    return dist_from_start


def part_1(lines: Iterable[list[str]]):
    maze = Matrix[str](list(lines))

    unvisited_cells = {t[0] for t in maze.find(lambda p, s: s != "#")}

    start_point = [c[0] for c in maze.find(lambda p, s: s == "S")][0]
    end_point = [c[0] for c in maze.find(lambda p, s: s == "E")][0]

    directed_graph = defaultdict[Vertex, list[Edge]](list[Edge])
    _build_cell_vertex_quads(maze, directed_graph)
    _connect_cells(maze, start_point, set(unvisited_cells), directed_graph)

    point_vertex_lookup = _build_point_vertex_lookup(directed_graph)
    start_vertex = [v for v in point_vertex_lookup[start_point] if v.direction == RIGHT][0]
    end_vertices = point_vertex_lookup[end_point]

    shortest = 999999999999
    shortest_paths = _shortest_paths(directed_graph, start_vertex)
    for end in end_vertices:
        # four possible end vertices, for each direction that it might be reached from
        shortest = min(shortest_paths[end], shortest)

    return shortest


run(16, part_1, parser=lambda s: [c for c in s])
