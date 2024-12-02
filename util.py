from typing import Callable


def get_input[T](filename: str, parser: Callable[[str], T]):
    with open(filename) as file:
        line = ""

        while True:
            line = file.readline()
            line = line.replace("\r", "").replace("\n", "")

            if line != "":
                yield parser(line)
            else:
                return


def get_int_pairs(line: str):
    line_values = [v for v in line.split(" ") if v != ""]

    return int(line_values[0]), int(line_values[1])


def run_for[TIn, TOut](filename: str, runner: Callable[[TIn], TOut]):
    print(f"{filename.ljust(28) } -> {runner(filename)}")
