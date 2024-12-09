from typing import Any, Callable
from util.types.point import Point
from util.matrix import get_dimensions


class Matrix[T]:
    __matrix: list[list[T]]

    def __init__(self, matrix: list[list[T]]):
        self.__matrix = matrix

    def __getitem__(self, item: Point):
        return self.__matrix[item.y][item.x]

    def __setitem__(self, item: Point, value: T):
        self.__matrix[item.y][item.x] = value

    def __format_row(self, row: list[T]):
        return " ".join(str(cell) for cell in row)

    def __str__(self):
        return "\n".join(self.__format_row(row) for row in self.__matrix)

    @staticmethod
    def __create_empty_row(width: int, default_value: T):
        return [default_value for _ in range(width)]

    @staticmethod
    def create_empty(width: int, height: int, default_value: T):
        rows = [Matrix.__create_empty_row(width, default_value) for _ in range(height)]

        return Matrix(rows)

    def width(self):
        return get_dimensions(self.__matrix)[0]

    def height(self):
        return get_dimensions(self.__matrix)[1]

    def visit(self, callback: Callable[[Point, T], Any]):
        for y in range(self.height()):
            for x in range(self.width()):
                yield callback(Point(x, y), self.__matrix[y][x])

    def is_out_of_bounds(self, p: Point):
        if p.x < 0 or p.x > self.width() - 1:
            return True

        if p.y < 0 or p.y > self.height() - 1:
            return True

        return False

    def walk_matrix(self, point: Point, diff: Point):
        """
        Creates a straight "path" through the matrix, from the given point, stepping over `diff` with each step
        """
        point = point + diff
        while not self.is_out_of_bounds(point):
            yield point

            point = point + diff
