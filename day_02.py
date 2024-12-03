from util import get_input, get_int_list, remove_at, run_for


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


def is_dampenable(unsafe_report: list[int]):
    # improve performance by only testing removal of elements which are known to fail the safety checks
    for i in range(len(unsafe_report)):
        if is_line_safe(remove_at(unsafe_report, i)):
            return True

    return False


def count_safe_lines(filename: str):
    lines = get_input(filename, get_int_list)

    return len(list(l for l in lines if is_line_safe(l)))


def count_dampenable_safe_lines(filename: str):
    lines = list(get_input(filename, get_int_list))
    unsafe_lines = [l for l in lines if not is_line_safe(l)]

    dampenable_count = len([l for l in unsafe_lines if is_dampenable(l)])

    unsafe_count = len(unsafe_lines) - dampenable_count
    safe_count = len(lines) - unsafe_count

    return safe_count


run_for(2, count_safe_lines, count_dampenable_safe_lines)
