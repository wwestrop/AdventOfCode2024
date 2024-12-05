from typing import Iterable

from util.collections import remove_at
from util.driver import run
from util.parser import get_int_list


def get_pairwise_difference(line: list[int]):
    for i in range(0, len(line) - 1):
        diff = abs(line[i] - line[i + 1])
        yield diff


def _is_line_safe(line: list[int]):
    unidirection = line == sorted(line) or line == list(reversed(sorted(line)))
    if not unidirection:
        return False

    for diff in get_pairwise_difference(line):
        if diff < 1 or diff > 3:
            return False

    return True


def _is_dampenable(unsafe_report: list[int]):
    # improve performance by only testing removal of elements which are known to fail the safety checks
    for i in range(len(unsafe_report)):
        if _is_line_safe(remove_at(unsafe_report, i)):
            return True

    return False


def count_safe_lines(lines: Iterable[list[int]]):
    return len(list(l for l in lines if _is_line_safe(l)))


def count_dampenable_safe_lines(lines: Iterable[list[int]]):
    lines = list(lines)
    unsafe_lines = [l for l in lines if not _is_line_safe(l)]

    dampenable_count = len([l for l in unsafe_lines if _is_dampenable(l)])

    unsafe_count = len(unsafe_lines) - dampenable_count
    safe_count = len(lines) - unsafe_count

    return safe_count


run(2, count_safe_lines, count_dampenable_safe_lines, parser=get_int_list)
