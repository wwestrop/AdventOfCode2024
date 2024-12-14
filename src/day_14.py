from dataclasses import dataclass
from typing import Iterable
from util.types.point import Point
from util.driver import run


@dataclass
class Robot:
    position: Point
    velocity: Point


def _parse(line: str):
    parts = line.replace("p=", "").replace("v=", "").split(" ")
    px, py = [int(n) for n in parts[0].split(",")]
    vx, vy = [int(n) for n in parts[1].split(",")]

    return Robot(
        position=Point(px, py),
        velocity=Point(vx, vy),
    )


def _step(robot: Robot, width: int, height: int):
    robot.position += robot.velocity

    x = robot.position.x
    y = robot.position.y

    if x >= width:
        x = abs(x) - width

    if y >= height:
        y = abs(y) - height

    if x < 0:
        x = width - abs(x)

    if y < 0:
        y = height - abs(y)

    robot.position = Point(x, y)


def _get_quadrants(robots: list[Robot], width, height):
    center_x, center_y = int(width / 2), int(height / 2)

    # NW
    yield [r for r in robots if r.position.x < center_x and r.position.y < center_y]

    # NE
    yield [r for r in robots if r.position.x > center_x and r.position.y < center_y]

    # SE
    yield [r for r in robots if r.position.x > center_x and r.position.y > center_y]

    # SW
    yield [r for r in robots if r.position.x < center_x and r.position.y > center_y]


def part_1(lines: Iterable[str]):
    robots = [_parse(l) for l in lines]

    width = list(sorted(r.position.x for r in robots))[-1] + 1
    height = list(sorted(r.position.y for r in robots))[-1] + 1

    for step in range(100):
        for r in robots:
            _step(r, width, height)

    quad_counts = [len(x) for x in _get_quadrants(robots, width, height)]
    safety_margin = 1
    for c in quad_counts:
        safety_margin *= c

    return safety_margin


run(14, part_1)
