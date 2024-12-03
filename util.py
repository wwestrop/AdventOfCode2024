from typing import Callable, Iterable


def _no_op(input):
    return input


def _get_input[T](filename: str, parser: Callable[[str], T]):
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


def run_for[TIn, TOut](
    day: int,
    runner1: Callable[[Iterable[TIn]], TOut],
    runner2: Callable[[Iterable[TIn]], TOut] | None = None,
    parser: Callable[[str], TIn] = _no_op,
):
    filename_prefix = "inputs/day"
    filename_suffix = ".txt"

    day_num = str(day).rjust(2, "0")
    example_file = filename_prefix + day_num + "-example" + filename_suffix
    input_file = filename_prefix + day_num + filename_suffix

    example_data = _get_input(example_file, parser)
    input_data = _get_input(input_file, parser)
    print(f"{example_file.ljust(28) } -> {runner1(example_data)}")
    print(f"{input_file.ljust(28) } -> {runner1(input_data)}")

    if runner2 is not None:
        print("--------------------------------------------------")
        example_data = _get_input(example_file, parser)
        input_data = _get_input(input_file, parser)
        print(f"{example_file.ljust(28) } -> {runner2(example_data)}")
        print(f"{input_file.ljust(28) } -> {runner2(input_data)}")


def remove_at[T](input: list[T], i: int) -> list[T]:
    copy = list(input)
    del copy[i]

    return copy
