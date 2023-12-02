from os import path
from typing import Literal, Iterable


def _load(puzzle_num: int, file_type: Literal["input", "example"]) -> Iterable[str]:
    file = path.join(path.realpath('.'), "inputs", f"{file_type}{puzzle_num}.txt")
    with open(file, "r") as f:
        return (line.strip() for line in f.readlines())


def load_input(puzzle_num: int) -> Iterable[str]:
    return _load(puzzle_num, 'input')


def load_example(puzzle_num: int) -> Iterable[str]:
    return _load(puzzle_num, 'example')
