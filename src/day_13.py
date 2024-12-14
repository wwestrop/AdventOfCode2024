from collections import defaultdict
from dataclasses import dataclass
import re
from typing import Iterable
from util.types.point import Point
from util.driver import run


@dataclass
class Machine:
    a: Point
    b: Point
    goal: Point


BUTTON_REGEX = re.compile("Button (?P<button>A|B): X\\+(?P<x>[0-9]+), Y\\+(?P<y>[0-9]+)")
GOAL_REGEX = re.compile("Prize: X=(?P<x>[0-9]+), Y=(?P<y>[0-9]+)")


def _parse(lines: Iterable[str]):
    for l in lines:
        buttons = BUTTON_REGEX.match(l)
        goal = GOAL_REGEX.match(l)

        a: Point
        b: Point
        if buttons:
            offset = Point(int(buttons.group("x")), int(buttons.group("y")))
            if buttons.group("button") == "A":
                a = offset
            else:
                b = offset
        elif goal:
            goal = Point(int(goal.group("x")), int(goal.group("y")))
            assert goal.x != 0
            assert goal.y != 0
            assert not (a.x == b.x and a.y == b.y)
            yield Machine(a, b, goal)


def _solve_machine(machine: Machine):
    origin = Point(0, 0)

    coordinate_costs = defaultdict[Point, dict[str, int]](dict[str, int])

    p = origin
    cost = 0
    while p.x <= machine.goal.x and p.y <= machine.goal.y:
        if p == machine.goal:
            # All A, no B
            assert False

        coordinate_costs[p]["A"] = cost
        p = p + machine.a
        cost += 3

    p = origin
    cost = 0
    while p.x <= machine.goal.x and p.y <= machine.goal.y:
        if p == machine.goal:
            # All B, no A
            assert False

        coordinate_costs[p]["B"] = cost
        p = p + machine.b
        cost += 1

    solutions = []

    # project rays out backwards
    p = machine.goal
    cost = 0
    while p.x >= origin.x and p.y >= origin.y:
        if "B" in coordinate_costs[p]:
            # found an intersection
            solutions.append((("B", coordinate_costs[p]["B"]), ("A", cost)))
            break

        p = p - machine.a
        cost += 3

    p = machine.goal
    while p.x >= origin.x and p.y >= origin.y:
        if "A" in coordinate_costs[p]:
            # found an intersection
            solutions.append((("A", coordinate_costs[p]["A"]), ("B", cost)))
            break

        p = p - machine.b
        cost += 1

    if len(solutions) == 2:
        sums = [x[0][1] + x[1][1] for x in solutions]
        return list(sorted(sums))[0]

    # no intersection found
    return -1


def part_1(lines: Iterable[str]):
    machines = _parse(lines)
    cost = 0
    for m in machines:
        machine_cost = _solve_machine(m)
        if machine_cost != -1:
            cost += machine_cost

    return cost


run(13, part_1)
