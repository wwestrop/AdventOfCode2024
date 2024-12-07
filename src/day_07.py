from dataclasses import dataclass
from typing import Iterable

import numpy

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


def _generate_operator_combos(possible_operators: list[str], number_of_operators: int):
    number_of_combos = len(possible_operators) ** number_of_operators

    for i in range(number_of_combos):
        num = numpy.base_repr(i, len(possible_operators)).rjust(number_of_operators, "0")
        digits = [int(b) for b in num]

        operator_combo = [possible_operators[b] for b in digits]
        yield operator_combo


def _evaluate(input: list):
    accum = input[0]

    operator = "+"
    for x in input[1:]:
        if x == "+":
            operator = "+"
        elif x == "*":
            operator = "*"
        elif x == "||":
            operator = "||"
        else:
            operand = int(x)
            if operator == "+":
                accum += operand
            elif operator == "||":
                accum = int(str(accum) + str(operand))
            else:
                accum *= operand

    return accum


def _has_solution(input: Input, possible_operators: list[str]):
    operator_combos = _generate_operator_combos(possible_operators, len(input.operands) - 1)

    for combo in operator_combos:
        candidate_equation = intersperse(input.operands, combo)
        if _evaluate(candidate_equation) == input.target:
            return True

    return False


def part_1(lines: Iterable[Input]):
    _OPERATORS = ["+", "*"]
    solvable_equations = [x for x in lines if _has_solution(x, _OPERATORS)]

    return sum(z.target for z in solvable_equations)


def part_2(lines: Iterable[Input]):
    _OPERATORS = ["+", "*", "||"]
    solvable_equations = [x for x in lines if _has_solution(x, _OPERATORS)]

    return sum(z.target for z in solvable_equations)


run(7, part_1, part_2, parser=_parse)
