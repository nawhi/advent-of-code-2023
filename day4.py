import unittest
from typing import Iterable

from loaders import load_input, load_example


def get_all_space_separated_numbers(line: str) -> Iterable[int]:
    return (int(n) for n in line.split(" ") if n)


def score_line(line: str) -> int:
    numbers_bit = line.split(": ")[1]
    my_numbers_raw, draw_numbers_raw = numbers_bit.split(" | ")
    draw_numbers = set(get_all_space_separated_numbers(draw_numbers_raw))
    my_numbers = get_all_space_separated_numbers(my_numbers_raw)

    num_matching_numbers = sum(1 for n in my_numbers if n in draw_numbers)

    if num_matching_numbers == 0:
        return 0
    return 2 ** (num_matching_numbers - 1)


def process_lines(lines: Iterable[str]):
    return sum(score_line(line) for line in lines)


DAY_NUM = 4


class Day1Test(unittest.TestCase):
    def test_example(self):
        lines = load_example(DAY_NUM)
        self.assertEqual(process_lines(lines), 13)

    def test_puzzle_1(self):
        lines = load_input(DAY_NUM)
        self.assertEqual(process_lines(lines), 21919)
