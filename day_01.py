from util import get_input, get_int_pairs, run_for


def pairwise_sum_difference(filename: str):
    lines = list(get_input(filename, get_int_pairs))

    list1 = sorted([v[0] for v in lines])
    list2 = sorted([v[1] for v in lines])

    diff = 0
    for pair in zip(list1, list2):
        diff += abs(pair[0] - pair[1])

    return diff


def calculate_incidence_map(list: list[int]):
    result: dict[int, int] = {}

    for item in list:
        if item in result:
            result[item] = result[item] + 1
        else:
            result[item] = 1

    return result


def similarity_score(filename: str):
    lines = list(get_input(filename, get_int_pairs))

    list1 = [v[0] for v in lines]
    list2 = [v[1] for v in lines]

    incidence_map = calculate_incidence_map(list2)

    similarity = 0
    for item in list1:
        incidences_in_list2 = incidence_map[item] if item in incidence_map else 0
        similarity += item * incidences_in_list2

    return similarity


run_for("inputs/day_01/example.txt", pairwise_sum_difference)
run_for("inputs/day_01/input.txt", pairwise_sum_difference)

print("-" * 50)

run_for("inputs/day_01/example.txt", similarity_score)
run_for("inputs/day_01/input.txt", similarity_score)
