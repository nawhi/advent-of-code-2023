import itertools
import unittest
from dataclasses import dataclass
from typing import List, Iterable, Union

from loaders import load_example, load_input


@dataclass
class Position:
    x: int
    y: int

    def __iter__(self):
        yield self.x
        yield self.y


@dataclass
class NumberPosition(Position):
    w: int

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.w


@dataclass
class PositionedNumber:
    value: int
    pos: NumberPosition


def find_numbers_in_line(string: str, y: int) -> Iterable[PositionedNumber]:
    ix = 0
    while ix < len(string):
        if string[ix].isdigit():
            start_ix = ix
            num_str = ""
            while ix < len(string) and string[ix].isdigit():
                num_str += string[ix]
                ix += 1
            yield PositionedNumber(int(num_str), NumberPosition(start_ix, y, ix - start_ix))
        ix += 1


def is_symbol(char: str) -> bool:
    return char is not None and char != '.' and not char.isdigit()


def soft_get_char(lines: List[str], pos: Position) -> Union[str, None]:
    x, y = pos
    if x < 0 or y < 0 or x >= len(lines[0]) or y >= len(lines):
        return None
    return lines[y][x]


def is_parts_number(pos: NumberPosition, lines: List[str]) -> bool:
    x, y, w = pos
    positions = [
        Position(x - 1, y),
        Position(x + w, y)
    ]
    for y1 in (y - 1, y + 1):
        for x1 in range(x - 1, x + w + 1):
            positions.append(Position(x1, y1))

    return any(is_symbol(soft_get_char(lines, pos)) for pos in positions)


def process_lines(lines: List[str]):
    numbers = itertools.chain.from_iterable(find_numbers_in_line(line, i) for i, line in enumerate(lines))
    parts_numbers = (pn for pn in numbers if is_parts_number(pn.pos, lines))
    return sum(pn.value for pn in parts_numbers)


DAY_NUM = 3


class Day1Test(unittest.TestCase):
    def test_find_number_at_start(self):
        nums = find_numbers_in_line("123...", 0)
        self.assertEqual([PositionedNumber(123, NumberPosition(0, 0, 3))], list(nums))

    def test_find_number_at_end(self):
        nums = find_numbers_in_line("......%.&.*.12345", 0)
        self.assertEqual([PositionedNumber(12345, NumberPosition(12, 0, 5))], list(nums))

    def test_find_two_numbers(self):
        nums = find_numbers_in_line(".%.&.*.1234...*..£.654321", 0)
        self.assertEqual([
            PositionedNumber(1234, NumberPosition(7, 0, 4)),
            PositionedNumber(654321, NumberPosition(19, 0, 6))
        ], list(nums))

    def test_find_numbers_different_y(self):
        nums = find_numbers_in_line("...123...456", 1)
        self.assertEqual([
            PositionedNumber(123, NumberPosition(3, 1, 3)),
            PositionedNumber(456, NumberPosition(9, 1, 3))
        ], list(nums))

    def test_is_adjacent_to_symbol_false(self):
        lines = [".0", ]
        self.assertEqual(is_parts_number(NumberPosition(0, 0, 1), lines), False)

    def test_is_adjacent_to_symbol_full_false_single(self):
        lines = [".....",
                 "..5..",
                 "....."]
        self.assertEqual(is_parts_number(NumberPosition(2, 2, 1), lines), False)

    def test_is_adjacent_to_symbol_full_false_multi(self):
        lines = [".......",
                 "..567..",
                 "......."]
        self.assertEqual(is_parts_number(NumberPosition(2, 2, 1), lines), False)

    def test_is_adjacent_to_symbol_true_left(self):
        lines = ["*0"]
        self.assertTrue(is_parts_number(NumberPosition(1, 0, 1), lines))

    def test_is_adjacent_to_symbol_true_right(self):
        lines = ["24*"]
        self.assertTrue(is_parts_number(NumberPosition(0, 0, 2), lines))

    def test_is_adjacent_to_symbol_true_diag(self):
        lines = [".....",
                 ".567.",
                 "....%"]
        self.assertTrue(is_parts_number(NumberPosition(1, 1, 3), lines))

    def test_example(self):
        lines = load_example(DAY_NUM)
        self.assertEqual(process_lines(list(lines)), 4361)

    def test_puzzle_1(self):
        lines = load_input(DAY_NUM)
        self.assertEqual(process_lines(list(lines)), 533775)
