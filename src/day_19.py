from collections import defaultdict
from typing import Iterable
from util.driver import run


def __parse(lines: Iterable[str]):
    lines = list(lines)

    towel_stock = lines[0].split(", ")
    patterns = lines[2:]

    return towel_stock, patterns


def _can_make_pattern(pattern: str, towel_stock: list[str]):
    can_solve_after = defaultdict[int, bool](lambda: False)
    can_solve_after[len(pattern)] = True  # empty suffix, base case

    for i in range(len(pattern) - 1, -1, -1):
        for t in towel_stock:
            towel_fits_here = pattern[i : i + len(t)] == t
            suffix_solvable = can_solve_after[i + len(t)]

            if towel_fits_here and suffix_solvable:
                can_solve_after[i] = True
                break

    return can_solve_after[0]


def part_1(lines: Iterable[str]):
    towel_stock, patterns = __parse(lines)

    return sum(_can_make_pattern(p, towel_stock) for p in patterns)


run(19, part_1)
