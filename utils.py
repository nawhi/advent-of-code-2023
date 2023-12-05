from typing import Iterable, List


def find_space_separated_integers(line: str) -> List[int]:
    return list(int(n) for n in line.split(" ") if n)


def dbg(thing):
    """ Wrapper around print() that eagerly evaluates generators/iterators """
    if hasattr(thing, '__iter__'):
        print(list(iter(thing)))
    else:
        print(thing)
