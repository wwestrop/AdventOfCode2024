import os
from typing import Callable, Iterable


def _no_op(input):
    return input


def _get_input[T](filename: str, parser: Callable[[str], T]) -> Iterable[T]:
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


def _run_for_file[TIn, TOut](filename: str, runner: Callable[[Iterable[TIn]], TOut], parser: Callable[[str], TIn]):
    input_data = _get_input(filename, parser) if os.path.isfile(filename) else None
    result = runner(input_data) if input_data is not None else "[X]"

    print(f"{filename.ljust(28) } -> {result}")


def _run_for[TIn, TOut](day: int, runner: Callable[[Iterable[TIn]], TOut], parser: Callable[[str], TIn]):
    day_num = str(day).rjust(2, "0")
    example_filename = f"inputs/day{day_num}-example.txt"
    input_filename = f"inputs/day{day_num}.txt"

    _run_for_file(example_filename, runner, parser)
    _run_for_file(input_filename, runner, parser)


def run[TIn, TOut](
    day: int,
    runner1: Callable[[Iterable[TIn]], TOut],
    runner2: Callable[[Iterable[TIn]], TOut] | None = None,
    parser: Callable[[str], TIn] = _no_op,
):
    _run_for(day, runner1, parser)

    if runner2 is not None:
        print("--------------------------------------------------")
        _run_for(day, runner2, parser)


def remove_at[T](input: list[T], i: int) -> list[T]:
    copy = list(input)
    del copy[i]

    return copy
