import unittest
from typing import List

from loaders import load_input, load_example


def process_lines(lines: List[str]):
    pass


DAY_NUM = 0


class Day1Test(unittest.TestCase):
    def test_example(self):
        lines = load_example(DAY_NUM)
        self.assertEqual(process_lines(lines), 0)

    def test_puzzle_1(self):
        lines = load_input(DAY_NUM)
        self.assertEqual(process_lines(lines), 0)
