from collections import defaultdict
from itertools import combinations
from typing import Iterable
from util.driver import run


def _parse(line: str):
    parts = line.split("-")
    return parts[0], parts[1]


def part_1(connection_lines: Iterable[tuple[str, str]]):
    connections = defaultdict[str, set[str]](set)

    for m in connection_lines:
        connections[m[0]].add(m[1])
        connections[m[1]].add(m[0])

    triplets = set[str]()
    for k, v in connections.items():
        if len(list(v)) < 2:
            continue

        other_computer_possibilities = combinations(v, 2)
        for p in other_computer_possibilities:
            if k.startswith("t") or p[0].startswith("t") or p[1].startswith("t"):
                if k in connections[p[0]] and k in connections[p[1]]:
                    if p[0] in connections[p[1]] and p[1] in connections[p[0]]:
                        triplet_str = ",".join(sorted([k, p[0], p[1]]))
                        triplets.add(triplet_str)

    return len(triplets)


run(23, part_1, parser=_parse)
