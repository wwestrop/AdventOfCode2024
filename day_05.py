from graphlib import TopologicalSorter
from typing import Iterable

from util import ordered_list_intersect, run, split_sequence


def topological_sort[T](edges: list[tuple[T, T]]):
    vertices = set([e[0] for e in edges] + [e[1] for e in edges])

    vertex_predecessor_dict = {v: [e[0] for e in edges if e[1] == v] for v in vertices}

    sorter = TopologicalSorter(vertex_predecessor_dict)

    return list(sorter.static_order())


def _is_manual_sorted(manual_pages: list[int], proper_page_order: list[int]):
    return list(ordered_list_intersect(proper_page_order, manual_pages)) == manual_pages


def sum_middle_pages_of_ordered_manuals(lines: Iterable[str]):
    # my plan of a generic parser for the input failed, this input comes in two parts
    # so here I am sorting it within the day's method

    raw_edges, raw_manuals = list(split_sequence(lines, ""))

    edges = [l.split("|") for l in raw_edges]
    edges = [(int(e[0]), int(e[1])) for e in edges]
    manuals = [p.split(",") for p in raw_manuals]
    manuals = [[int(p) for p in e] for e in manuals]

    proper_page_order = topological_sort(edges)

    sorted_manuals = [m for m in manuals if _is_manual_sorted(m, proper_page_order)]

    midpoints = [x[int(len(x) / 2)] for x in sorted_manuals]

    return sum(midpoints)


run(5, sum_middle_pages_of_ordered_manuals)
