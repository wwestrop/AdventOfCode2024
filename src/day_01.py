from typing import Iterable

from util.driver import run
from util.parser import get_int_pairs


def pairwise_sum_difference(lines: Iterable[tuple[int, int]]):
    lines = list(lines)
    list1 = sorted([v[0] for v in lines])
    list2 = sorted([v[1] for v in lines])

    diff = 0
    for pair in zip(list1, list2):
        diff += abs(pair[0] - pair[1])

    return diff


def _calculate_incidence_map(list: list[int]):
    result: dict[int, int] = {}

    for item in list:
        if item in result:
            result[item] = result[item] + 1
        else:
            result[item] = 1

    return result


def similarity_score(lines: Iterable[tuple[int, int]]):
    lines = list(lines)
    list1 = [v[0] for v in lines]
    list2 = [v[1] for v in lines]

    incidence_map = _calculate_incidence_map(list2)

    similarity = 0
    for item in list1:
        incidences_in_list2 = incidence_map[item] if item in incidence_map else 0
        similarity += item * incidences_in_list2

    return similarity


run(1, pairwise_sum_difference, similarity_score, parser=get_int_pairs)
