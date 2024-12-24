from dataclasses import dataclass
import re
from typing import Iterable, Literal
from util.driver import run


@dataclass
class Operation:
    operand_1: str
    operator: Literal["XOR"] | Literal["OR"] | Literal["AND"]
    operand_2: str
    output: str


_OPERATION_FINDER = re.compile(
    "(?P<operand_1>[a-zA-Z0-9]+) (?P<operator>[a-zA-Z0-9]+) (?P<operand_2>[a-zA-Z0-9]+) -> (?P<output>[a-zA-Z0-9]+)"
)


def _parse(lines: Iterable[str]):
    lines = list(lines)

    split = lines.index("")

    initial_values = lines[:split]
    raw_operations = lines[split + 1 :]

    resolved_values = {s[0]: int(s[1]) for s in (v.split(": ") for v in initial_values)}

    operations: list[Operation] = []
    for op in raw_operations:
        regex_match = _OPERATION_FINDER.match(op)
        operation = Operation(
            regex_match.group("operand_1"),
            regex_match.group("operator"),
            regex_match.group("operand_2"),
            regex_match.group("output"),
        )
        operations.append(operation)

    return resolved_values, operations


def _resolve_output_wires(operations: list[Operation], resolved_values: dict[str, int]):
    for i in range(len(operations) - 1, -1, -1):
        op = operations[i]

        # is operands are resolvable
        if op.operand_1 in resolved_values and op.operand_2 in resolved_values:
            del operations[i]
            match op.operator:
                case "AND":
                    resolved_values[op.output] = resolved_values[op.operand_1] & resolved_values[op.operand_2]
                case "OR":
                    resolved_values[op.output] = resolved_values[op.operand_1] | resolved_values[op.operand_2]
                case "XOR":
                    resolved_values[op.output] = resolved_values[op.operand_1] ^ resolved_values[op.operand_2]


def _bin2dec(bits: list[int]):
    pos = 0
    result = 0
    for b in bits:
        pos_value = pow(2, pos)
        result += b * pos_value
        pos += 1

    return result


def part_1(lines: Iterable[str]):
    resolved_values, operations = _parse(lines)

    final_outputs = (g.output for g in operations if g.output.startswith("z"))
    final_outputs = list(sorted(final_outputs, key=lambda o: int(o[1:])))

    while any(k for k in final_outputs if k not in resolved_values):
        _resolve_output_wires(operations, resolved_values)

    z_outputs = [resolved_values[z] for z in final_outputs]
    return _bin2dec(z_outputs)


run(24, part_1)
