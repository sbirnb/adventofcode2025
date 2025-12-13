import sys
from typing import Iterable, Tuple, Sequence
import re


def parse_input(input_: Iterable[str]) -> Tuple[Sequence[Sequence[complex]], Sequence[Tuple[Tuple[int, int], Sequence[int]]]]:
    lines = map(str.strip, input_)
    footprints, areas = [], []
    for _ in range(6):
        next(lines)
        footprints.append(tuple(complex(row, col) for row, cols in zip(range(3), lines) for col, val in enumerate(cols) if val == '#'))
        next(lines)
    for line in lines:
        str_l, str_w, qtys = re.match(r'(\d+)x(\d+): ((?:\d+ ?)+)', line).groups()
        areas.append(((int(str_l), int(str_w)), tuple(map(int, qtys.split()))))
    return footprints, areas


def part1(input_: Iterable[str]) -> int:
    footprints, areas = parse_input(input_)
    sizes = list(map(len, footprints))
    return sum(sum(quantity * size for quantity, size in zip(quantities, sizes)) <= width * height for (width, height), quantities in areas)


def part2(input_: Iterable[str]) -> int:
    pass


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))