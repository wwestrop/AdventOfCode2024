from typing import Iterable

from util.collections import ordered_list_intersect, split_sequence, topological_sort
from util.driver import run


def _vertex_filter[T](graph: list[tuple[T, T]], relevant_vertices: list[T]):
    """
    For the given graph, strip out every vertex and its edges unless
    they are in the `relevant_vertices` list, and return the new graph
    """
    return [e for e in graph if e[0] in relevant_vertices and e[1] in relevant_vertices]


def _get_proper_sort_order(manual_pages: list[int], page_order_graph: list[tuple[int, int]]):
    relevant_graph = _vertex_filter(page_order_graph, manual_pages)

    proper_page_order = topological_sort(relevant_graph)

    relevant_proper_page_order = list(ordered_list_intersect(proper_page_order, manual_pages))

    return relevant_proper_page_order


def _is_manual_sorted(manual_pages: list[int], page_order_graph: list[tuple[int, int]]):
    return _get_proper_sort_order(manual_pages, page_order_graph) == manual_pages


# my plan of a generic parser for the input failed, as it assumes parsing is done linewise.
# this input comes in two parts, so I'm doing it within the day's solution
def _parse_input(lines: Iterable[str]):
    raw_edges, raw_manuals = list(split_sequence(lines, ""))

    edges = [l.split("|") for l in raw_edges]
    edges = [(int(e[0]), int(e[1])) for e in edges]
    manuals = [p.split(",") for p in raw_manuals]
    manuals = [[int(p) for p in e] for e in manuals]

    return edges, manuals


def sum_middle_pages_of_ordered_manuals(lines: Iterable[str]):
    edges, manuals = _parse_input(lines)

    sorted_manuals = [m for m in manuals if _is_manual_sorted(m, edges)]

    midpoints = [x[int(len(x) / 2)] for x in sorted_manuals]

    return sum(midpoints)


def reorder_manuals(lines: Iterable[str]):
    edges, manuals = _parse_input(lines)

    unsorted_manuals = [m for m in manuals if not _is_manual_sorted(m, edges)]

    resorted_manuals = [_get_proper_sort_order(m, edges) for m in unsorted_manuals]

    midpoints = [x[int(len(x) / 2)] for x in resorted_manuals]

    return sum(midpoints)


run(5, sum_middle_pages_of_ordered_manuals, reorder_manuals)
