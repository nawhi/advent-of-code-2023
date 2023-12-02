import unittest
from typing import List

from loaders import load_input, load_example


def integer_of_first_and_last_digit(line: str) -> int:
    first_digit = next(s for s in line if s.isdigit())
    last_digit = next(s for s in reversed(line) if s.isdigit())
    return int(first_digit + last_digit)


def sum_first_and_last_digit_per_line(lines: List[str]) -> int:
    return sum(integer_of_first_and_last_digit(line) for line in lines)


class Day1Test(unittest.TestCase):
    def test_example(self):
        lines = load_example(1)
        self.assertEqual(sum_first_and_last_digit_per_line(lines), 142)

    def test_puzzle_1(self):
        lines = load_input(1)
        self.assertEqual(sum_first_and_last_digit_per_line(lines), 54877)
