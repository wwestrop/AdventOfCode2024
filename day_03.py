import re

from util import get_input, run_for


_FUNCTION_FINDER = re.compile("mul\\((?P<op1>\\d{1,3}),(?P<op2>\\d{1,3})\\)")


def evaluate_instructions(filename: str):
    lines = list(get_input(filename))

    result = 0

    for line in lines:
        for func_call in _FUNCTION_FINDER.finditer(line):
            op1 = int(func_call.group("op1"))
            op2 = int(func_call.group("op2"))

            result += op1 * op2

    return result


run_for(3, evaluate_instructions)
