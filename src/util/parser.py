from util.types.point import Point


def get_int_list(line: str):
    return [int(v) for v in line.split(" ") if v != ""]


def get_int_pairs(line: str):
    line_values = [v for v in line.split(" ") if v != ""]

    return int(line_values[0]), int(line_values[1])


def get_points(line: str):
    coordinates = [int(p) for p in line.split(",")]
    return Point(coordinates[0], coordinates[1])
