from dataclasses import dataclass
from typing import Any, Iterable
from util.parser import get_int_list
from util.driver import run


@dataclass
class LinkedList[T]:
    value: T
    next: Any | None  #: LinkedList[T] | None

    def __len__(self):
        head = self
        count = 0
        while head is not None:
            count += 1
            head = head.next

        return count

    @staticmethod
    def build(input: list[T]):
        first_node = LinkedList(input[0], None)
        previous_node = first_node

        for i in range(1, len(input)):
            n = LinkedList(input[i], None)
            previous_node.next = n
            previous_node = n

        return first_node


def _split_digits(num: int):
    snum = str(num)
    half = int(len(snum) / 2)

    return int(snum[:half]), int(snum[half:])


def _blink(stones: LinkedList[int]):
    head = stones
    while head is not None:
        if head.value == 0:
            head.value = 1
        elif len(str(head.value)) % 2 == 0:
            left_half, right_half = _split_digits(head.value)
            head.value = left_half
            head.next = LinkedList(right_half, head.next)
            head = head.next  # skip 2
        else:
            head.value *= 2024

        head = head.next


# def lpr(ll):
#     r = ""
#     while ll is not None:
#         r += f"{ll.value} "
#         ll = ll.next

#     return r


def part_1(lines: Iterable[list[int]]):
    stones = LinkedList[int].build(list(lines)[0])

    for _ in range(25):
        _blink(stones)

    return len(stones)


run(11, part_1, parser=get_int_list)
