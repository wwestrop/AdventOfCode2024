from typing import Callable


def _no_op(input):
    return input


def get_input[T](filename: str, parser: Callable[[str], T] = _no_op):
    with open(filename) as file:
        line = ""

        while True:
            line = file.readline()
            line = line.replace("\r", "").replace("\n", "")

            if line != "":
                yield parser(line)
            else:
                return


def get_int_list(line: str):
    return [int(v) for v in line.split(" ") if v != ""]


def get_int_pairs(line: str):
    line_values = [v for v in line.split(" ") if v != ""]

    return int(line_values[0]), int(line_values[1])


def run_for[TOut](
    day: int,
    runner1: Callable[[str], TOut],
    runner2: Callable[[str], TOut] | None = None,
):
    filename_prefix = "inputs/day"
    filename_suffix = ".txt"

    day_num = str(day).rjust(2, "0")
    example_file = filename_prefix + day_num + "-example" + filename_suffix
    input_file = filename_prefix + day_num + filename_suffix

    print(f"{example_file.ljust(28) } -> {runner1(example_file)}")
    print(f"{input_file.ljust(28) } -> {runner1(input_file)}")

    if runner2 is not None:
        print("--------------------------------------------------")
        print(f"{example_file.ljust(28) } -> {runner2(example_file)}")
        print(f"{input_file.ljust(28) } -> {runner2(input_file)}")


def remove_at[T](input: list[T], i: int) -> list[T]:
    copy = list(input)
    del copy[i]

    return copy
