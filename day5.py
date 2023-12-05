import itertools
import re
import unittest
from dataclasses import dataclass
from typing import Iterable, List, Tuple

from loaders import load_input, load_example
from utils import dbg, find_space_separated_integers


@dataclass
class MapEntry:
    dest_range_start: int
    source_range_start: int
    range_length: int

    def convert(self, source):
        if self.source_range_start <= source < self.source_range_start + self.range_length:
            diff = source - self.source_range_start
            return self.dest_range_start + diff
        return source


@dataclass
class Map:
    source: str
    destination: str
    entries: List[MapEntry]

    def convert(self, source):
        for entry in self.entries:
            converted = entry.convert(source)
            if converted != source:
                return converted
        return source


def raw_to_entry_tuple(raw: str) -> Tuple[int, int, int]:
    one, two, three = find_space_separated_integers(raw)
    return one, two, three


def is_non_empty_string(line: str) -> bool:
    return len(line) > 0


re_x_to_y = re.compile("([a-z]+)-to-([a-z]+) map:")


def extract_maps_in_order(inputs: Iterable[str]) -> List[Map]:
    lines = list(inputs)
    outputs = []
    for i, line in enumerate(lines):
        header_match = re_x_to_y.match(line)
        if header_match:
            entry_lines = (itertools.takewhile(is_non_empty_string, lines[i + 1:]))
            entries = list(raw_to_entry_tuple(line) for line in entry_lines)
            outputs.append(
                Map(header_match.group(1), header_match.group(2), list(MapEntry(*entry) for entry in entries)))

    return outputs


def process_lines(lines: Iterable[str]):
    seed_nums_raw, *maps_raw = lines
    seed_nums = find_space_separated_integers(seed_nums_raw.split("seeds: ")[1])
    maps = extract_maps_in_order(maps_raw)

    converted_seed_nums = seed_nums
    for m in maps:
        converted_seed_nums = list(m.convert(n) for n in converted_seed_nums)

    return min(converted_seed_nums)


DAY_NUM = 5


class Day1Test(unittest.TestCase):

    def test_extract_maps(self):
        lines = load_example(DAY_NUM)
        self.assertEqual(extract_maps_in_order(lines)[:2], [
            Map("seed", "soil", [MapEntry(50, 98, 2), MapEntry(52, 50, 48)]),
            Map("soil", "fertilizer", [MapEntry(0, 15, 37), MapEntry(37, 52, 2), MapEntry(39, 0, 15)])
        ])

    def test_convert(self):
        entry = MapEntry(50, 98, 2)
        self.assertEqual(entry.convert(97), 97)
        self.assertEqual(entry.convert(100), 100)
        self.assertEqual(entry.convert(98), 50)
        self.assertEqual(entry.convert(99), 51)

    def test_convert_2(self):
        entry = MapEntry(52, 50, 48)
        self.assertEqual(entry.convert(53), 55)
        self.assertEqual(entry.convert(52), 54)

    def test_example(self):
        lines = load_example(DAY_NUM)
        self.assertEqual(process_lines(lines), 35)

    def test_puzzle_1(self):
        lines = load_input(DAY_NUM)
        self.assertEqual(process_lines(lines), 600279879)
