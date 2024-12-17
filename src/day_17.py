from dataclasses import dataclass
from enum import Enum
from typing import Iterable
from util.driver import run


class Instructions(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


@dataclass
class MachineState:
    A: int
    B: int
    C: int


def _combo_operand_value(operand: int, machine_state: MachineState):
    if operand <= 3:
        return operand

    if operand == 4:
        return machine_state.A
    if operand == 5:
        return machine_state.B
    if operand == 6:
        return machine_state.C

    if operand == 7:
        assert False, "Invalid program, combo operand 7 used"


def _strip_label(line: str):
    return line[line.find(": ") + 2 :]


def _parse(lines: Iterable[str]):
    lines = list(lines)

    register_a = int(int(_strip_label(lines[0])))
    register_b = int(int(_strip_label(lines[1])))
    register_c = int(int(_strip_label(lines[2])))

    program = _strip_label(lines[4])
    program = program.split(",")
    program = [int(op) for op in program]

    return MachineState(register_a, register_b, register_c), program


def part_1(lines: Iterable[str]):
    machine_state, program = _parse(lines)

    output = []

    i = 0
    while i < len(program):
        instruction = program[i]
        operand = program[i + 1]

        match instruction:
            case Instructions.ADV.value:
                numerator = machine_state.A
                denominator = 2 ** _combo_operand_value(operand, machine_state)
                machine_state.A = int(numerator / denominator)
            case Instructions.BXL.value:
                machine_state.B = machine_state.B ^ operand
            case Instructions.BST.value:
                machine_state.B = int(_combo_operand_value(operand, machine_state) % 8)
            case Instructions.JNZ.value:
                if machine_state.A != 0:
                    i = operand
                    continue
            case Instructions.BXC.value:
                machine_state.B = machine_state.B ^ machine_state.C
            case Instructions.OUT.value:
                opvalue = _combo_operand_value(operand, machine_state)
                output.append(str(int(opvalue % 8)))
            case Instructions.BDV.value:
                numerator = machine_state.A
                denominator = 2 ** _combo_operand_value(operand, machine_state)
                machine_state.B = int(numerator / denominator)
            case Instructions.CDV.value:
                # todo consolidate *dv instructions
                numerator = machine_state.A
                denominator = 2 ** _combo_operand_value(operand, machine_state)
                machine_state.C = int(numerator / denominator)

        i += 2

    return ",".join(output)


run(17, part_1)
