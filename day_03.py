import re

from util import get_input, run_for


def evaluate_instructions(filename: str):
    _FUNCTION_FINDER = re.compile("mul\\((?P<op1>\\d{1,3}),(?P<op2>\\d{1,3})\\)")
    lines = list(get_input(filename))

    result = 0

    for line in lines:
        for func_call in _FUNCTION_FINDER.finditer(line):
            op1 = int(func_call.group("op1"))
            op2 = int(func_call.group("op2"))

            result += op1 * op2

    return result


def evaluate_instructions_2(filename: str):
    _FUNCTION_FINDER = re.compile("(?P<func>[a-z']+)\\((?P<operands>[0-9,]*)\\)")
    lines = list(get_input(filename))

    enabled = True
    result = 0

    for line in lines:
        for func_call in _FUNCTION_FINDER.finditer(line):
            func = func_call.group("func")
            if func.endswith("do"):
                enabled = True
            elif func.endswith("don't"):
                enabled = False
            elif func.endswith("mul"):
                if enabled:
                    operands = [int(o) for o in func_call.group("operands").split(",")]

                    if len(operands) == 2:
                        result += operands[0] * operands[1]

    return result


run_for(3, evaluate_instructions, evaluate_instructions_2)
