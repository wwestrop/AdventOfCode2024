from graphlib import TopologicalSorter
from typing import Iterable

from util import ordered_list_intersect, run, split_sequence


def topological_sort[T](edges: list[tuple[T, T]]):
    vertices = set([e[0] for e in edges] + [e[1] for e in edges])

    vertex_predecessor_dict = {v: [e[0] for e in edges if e[1] == v] for v in vertices}

    sorter = TopologicalSorter(vertex_predecessor_dict)

    return list(sorter.static_order())


def _vertex_filter[T](graph: list[tuple[T, T]], relevant_vertices: list[T]):
    """
    For the given graph, strip out every vertex and its edges unless
    they are in the `relevant_vertices` list, and return the new graph
    """
    return [e for e in graph if e[0] in relevant_vertices and e[1] in relevant_vertices]


def _is_manual_sorted(manual_pages: list[int], page_order_graph: list[tuple[int, int]]):
    relevant_graph = _vertex_filter(page_order_graph, manual_pages)

    proper_page_order = topological_sort(relevant_graph)

    relevant_proper_page_order = list(ordered_list_intersect(proper_page_order, manual_pages))

    return relevant_proper_page_order == manual_pages


def sum_middle_pages_of_ordered_manuals(lines: Iterable[str]):
    # my plan of a generic parser for the input failed, this input comes in two parts
    # so here I am sorting it within the day's method

    raw_edges, raw_manuals = list(split_sequence(lines, ""))

    edges = [l.split("|") for l in raw_edges]
    edges = [(int(e[0]), int(e[1])) for e in edges]
    manuals = [p.split(",") for p in raw_manuals]
    manuals = [[int(p) for p in e] for e in manuals]

    sorted_manuals = [m for m in manuals if _is_manual_sorted(m, edges)]

    midpoints = [x[int(len(x) / 2)] for x in sorted_manuals]

    return sum(midpoints)


run(5, sum_middle_pages_of_ordered_manuals)
