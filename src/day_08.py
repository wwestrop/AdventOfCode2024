from itertools import combinations, groupby
from typing import Iterable

from util.types.matrix import Matrix
from util.driver import run


def part_1(input_lines: Iterable[str]):
    input = [list(line) for line in input_lines]

    emitter_map = Matrix(input)

    raw_frequency_locations = [t for t in emitter_map.visit(lambda p, i: (p, i)) if t[1] != "."]
    frequency_lookup = groupby(raw_frequency_locations, lambda f: f[1])

    antinode_map = Matrix.create_empty(emitter_map.width(), emitter_map.height(), default_value=False)

    for f, g in frequency_lookup:
        all_locations_of_this_frequency = list(g)

        frequency_pairs = list(combinations(all_locations_of_this_frequency, 2))
        for pair in frequency_pairs:
            e1 = pair[0][0]
            e2 = pair[1][0]
            distance = e2 - e1
            candidate_antinode_1 = e1 + distance * -1
            candidate_antinode_2 = e1 + distance * 2

            if not antinode_map.is_out_of_bounds(candidate_antinode_1):
                antinode_map[candidate_antinode_1] = True

            if not antinode_map.is_out_of_bounds(candidate_antinode_2):
                antinode_map[candidate_antinode_2] = True

    return sum(antinode_map.visit(lambda p, v: v))


run(8, part_1)
