from dataclasses import dataclass
from typing import Iterable

from util.collections import intersperse
from util.driver import run


@dataclass(frozen=True)
class Input:
    target: int
    operands: list[int]


def _parse(line: str):
    parts = line.split(": ")

    return Input(
        target=int(parts[0]),
        operands=[int(i) for i in parts[1].split(" ")],
    )


_OPERATORS = ["+", "*"]


def _generate_operator_combos(number_of_operators: int):
    number_of_combos = len(_OPERATORS) ** number_of_operators

    for i in range(number_of_combos):
        # I've given up on a generic counter and am assuming two operators
        # It will break otherwise
        num = bin(i)[2:].rjust(number_of_operators, "0")
        digits = [int(b) for b in num]

        operator_combo = [_OPERATORS[b] for b in digits]
        yield operator_combo


def _evaluate(input: list):
    accum = input[0]

    operator = "+"
    for x in input[1:]:
        if x == "+":
            operator = "+"
        elif x == "*":
            operator = "*"
        else:
            operand = int(x)
            if operator == "+":
                accum += operand
            else:
                accum *= operand

    return accum


def _has_solution(input: Input):
    operator_combos = _generate_operator_combos(len(input.operands) - 1)

    for combo in operator_combos:
        candidate_equation = intersperse(input.operands, combo)
        if _evaluate(candidate_equation) == input.target:
            return True

    return False


def part_1(lines: Iterable[Input]):
    solvable_equations = [x for x in lines if _has_solution(x)]

    return sum(z.target for z in solvable_equations)


run(7, part_1, parser=_parse)
