from graphlib import TopologicalSorter
from typing import Iterable


def remove_at[T](input: list[T], i: int) -> list[T]:
    copy = list(input)
    del copy[i]

    return copy


def split_sequence[T](input: Iterable[T], splitter: T):
    accumulator = []

    for i in input:
        if i == splitter:
            yield accumulator
            accumulator = []
        else:
            accumulator.append(i)

    yield accumulator


def ordered_list_intersect(list1: list, list2: list):
    """
    Finds the comment elements between two lists, keeping list1 in the same order
    """
    for x in list1:
        if x in list2:
            yield x


def topological_sort[T](edges: list[tuple[T, T]]):
    vertices = set([e[0] for e in edges] + [e[1] for e in edges])

    vertex_predecessor_dict = {v: [e[0] for e in edges if e[1] == v] for v in vertices}

    sorter = TopologicalSorter(vertex_predecessor_dict)

    return list(sorter.static_order())


def intersperse(list: list, intersperse_with: list):
    """
    Merge one list into another, putting elements from the second array in between
    elements in the first. Kind of like a zipper, except zip() already does something else
    """
    result = []

    for i in range(len(list)):
        result.append(list[i])

        if i < len(intersperse_with):
            result.append(intersperse_with[i])

    return result
