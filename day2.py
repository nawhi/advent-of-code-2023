import re
import unittest
from typing import Iterable, Literal

from loaders import load_input, load_example


class CubeBag:
    red: int
    green: int
    blue: int

    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue

    def set(self, colour: Literal["red", "green", "blue"], value: int):
        if value > self.__getattribute__(colour):
            self.__setattr__(colour, value)


re_game_id = re.compile(r"Game (\d+)")
re_cube_bag = re.compile(r"(\d+) (green|blue|red)")

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14


def cube_bag_of_line(line: str):
    bag = CubeBag()
    rounds = line.split(": ")[1].split("; ")
    for round in rounds:
        entries = round.split(", ")
        for entry in entries:
            match = re_cube_bag.match(entry)
            num_cubes, colour = int(match.group(1)), match.group(2)
            bag.set(colour, num_cubes)
    return bag


def is_valid_line(line: str) -> bool:
    bag = cube_bag_of_line(line)
    return bag.red <= MAX_RED and bag.green <= MAX_GREEN and bag.blue <= MAX_BLUE


def game_id_of_line(game: str) -> int:
    return int(re_game_id.search(game).group(1))


def process_lines(lines: Iterable[str]):
    return sum(game_id_of_line(line) for line in lines if is_valid_line(line))


def power_cube(cube: CubeBag):
    return cube.red * cube.green * cube.blue


def process_lines_2(lines: Iterable[str]):
    return sum(power_cube(cube_bag_of_line(line)) for line in lines)


DAY_NUM = 2


class Day1Test(unittest.TestCase):
    def test_example_1(self):
        lines = load_example(DAY_NUM)
        self.assertEqual(process_lines(lines), 8)

    def test_puzzle_1(self):
        lines = load_input(DAY_NUM)
        self.assertEqual(process_lines(lines), 2164)

    def test_example_2(self):
        lines = load_example(DAY_NUM)
        self.assertEqual(process_lines_2(lines), 2286)

    def test_puzzle_2(self):
        lines = load_input(DAY_NUM)
        self.assertEqual(process_lines_2(lines), 69929)
