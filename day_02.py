from util import get_input, get_int_list, run_for


def get_pairwise_difference(line: list[int]):
    for i in range(0, len(line) - 1):
        diff = abs(line[i] - line[i + 1])
        yield diff


def is_line_safe(line: list[int]):
    unidirection = line == sorted(line) or line == list(reversed(sorted(line)))
    if not unidirection:
        return False

    for diff in get_pairwise_difference(line):
        if diff < 1 or diff > 3:
            return False

    return True


def count_safe_lines(filename: str):
    lines = get_input(filename, get_int_list)

    return len(list(l for l in lines if is_line_safe(l)))


run_for(2, count_safe_lines)
