from util import get_input, get_int_pairs, run_for


def day_01(filename: str):
    lines = list(get_input(filename, get_int_pairs))

    list1 = sorted([v[0] for v in lines])
    list2 = sorted([v[1] for v in lines])

    diff = 0
    for pair in zip(list1, list2):
        diff += abs(pair[0] - pair[1])

    return diff


run_for("inputs/day_01/example.txt", day_01)
run_for("inputs/day_01/part1.txt", day_01)
