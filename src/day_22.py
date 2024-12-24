from typing import Iterable
from util.driver import run


def _calculate_next_sequence(secret_number: int):
    res = secret_number * 64
    secret_number = res ^ secret_number
    secret_number = secret_number % 16777216

    res2 = int(secret_number / 32)
    secret_number = res2 ^ secret_number
    secret_number = secret_number % 16777216

    res3 = secret_number * 2048
    secret_number = res3 ^ secret_number
    secret_number = secret_number % 16777216

    return secret_number


def part_1(lines: Iterable[int]):
    total = 0
    for secret_number in lines:
        result = secret_number
        for _ in range(2000):
            result = _calculate_next_sequence(result)

        total += result

    return total


run(22, part_1, parser=int)
