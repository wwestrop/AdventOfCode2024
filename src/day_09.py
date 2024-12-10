from dataclasses import dataclass
from typing import Iterable
from util.driver import run


@dataclass()
class Gap:
    size: int
    ptr: int


@dataclass()
class File:
    id: int
    size: int
    ptr: int


def _initialise_disk(input: str):
    chars = [int(x) for x in input]
    files = number_list(chars[::2])
    gaps = chars[1::2]

    disk = []
    gaps_and_ptrs: list[Gap] = []
    files_and_ptrs: list[File] = []

    ptr = 0
    for f in range(len(files)):
        file = files[f]
        file = File(file[0], file[1], ptr)
        files_and_ptrs.append(file)
        _write_file(disk, file.id, file.size)
        ptr += file.size

        if f != len(files) - 1:
            g = gaps[f]
            gaps_and_ptrs.append(Gap(g, ptr))
            _write_gap(disk, g)
            ptr += g

    return disk, files_and_ptrs, gaps_and_ptrs


def _write_file(disk: list[int], file_id: int, file_length: int):
    for i in range(file_length):
        disk.append(file_id)


def _overwrite_file(disk: list[int], ptr: int, file_id: int, bytes: int):
    for i in range(ptr, ptr + bytes):
        disk[i] = file_id


def _deallocate_from_file(disk: list[int], file: File, bytes: int):
    file_end = file.ptr + file.size
    for i in range(file_end - bytes, file_end):
        disk[i] = -1


def _write_gap(disk: list[int], gap_length: int):
    for i in range(gap_length):
        disk.append(-1)


def _find_first_contiguous_gap(gaps: list[Gap], file: File):
    for g in gaps:
        if g.size >= file.size:
            return g

    return None


def _find_next_gap(gaps: list[Gap], current_gap_index: int):
    """
    Get the next available gap with space in it. Could be the the current gap if it's not full
    """
    while gaps[current_gap_index].size == 0:
        current_gap_index += 1

    return current_gap_index


def number_list[T](input: list[T]) -> list[tuple[int, T]]:
    return list(zip(range(len(input)), input))


def _checksum(disk: list[int]):
    accum = 0

    for i in range(len(disk)):
        if disk[i] != -1:
            accum += i * disk[i]

    return accum


def _can_move(gaps: list[Gap], file: File):
    return any(g for g in gaps if g.size >= file.size)


def part_1(lines: Iterable[tuple[list[int], list[File], list[Gap]]]):
    disk, files, gaps = list(lines)[0]

    file_index = len(files) - 1
    gap_index = _find_next_gap(gaps, 0)
    write_ptr = gaps[gap_index].ptr

    file = files[file_index]
    gap = gaps[gap_index]
    while file.ptr > write_ptr:
        amount_to_write = min(gap.size, file.size)

        _overwrite_file(disk, write_ptr, file.id, amount_to_write)
        _deallocate_from_file(disk, file, amount_to_write)

        gap.size -= amount_to_write
        file.size -= amount_to_write

        write_ptr += amount_to_write

        if file.size == 0:
            file_index -= 1
            file = files[file_index]

        if gap.size == 0:
            gap_index = _find_next_gap(gaps, gap_index)
            gap = gaps[gap_index]
            write_ptr = gap.ptr

    return _checksum(disk)


def part_2(lines: Iterable[tuple[list[int], list[File], list[Gap]]]):
    disk, files, gaps = list(lines)[0]

    moveable_files = files[1:]
    file_index = len(moveable_files) - 1

    file = moveable_files[file_index]
    gap: Gap = _find_first_contiguous_gap(gaps, file)
    while any(_can_move(gaps, f) for f in moveable_files):
        for f in reversed(moveable_files):
            gap = _find_first_contiguous_gap(gaps, f)

            if gap is not None:
                amount_to_write = f.size

                _overwrite_file(disk, gap.ptr, f.id, amount_to_write)
                _deallocate_from_file(disk, f, amount_to_write)

                gap.size -= amount_to_write
                gap.ptr += amount_to_write
                f.size -= amount_to_write
                moveable_files.remove(f)

    return _checksum(disk)


run(9, part_1, part_2, parser=_initialise_disk)
