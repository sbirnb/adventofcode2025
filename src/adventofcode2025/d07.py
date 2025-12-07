import sys
from typing import Iterable


def part1(input_: Iterable[str]) -> int:
    rows = iter(input_)
    beams = [c == 'S' for c in next(rows).strip()]
    splits = 0
    for row in map(str.strip, rows):
        for i, (col, beam) in enumerate(zip(row, beams[:])):
            if beam and col == '^':
                splits += 1
                beams[i + 1] = beams[i - 1] = True
                beams[i] = False
    return splits


def part2(input_: Iterable[str]) -> int:
    rows = iter(input_)
    beams = [1 if c == 'S' else 0 for c in next(rows).strip()]
    for row in map(str.strip, rows):
        for i, (col, beam) in enumerate(zip(row, beams[:])):
            if beam and col == '^':
                beams[i + 1] += beam
                beams[i - 1] += beam
                beams[i] = 0
    return sum(beams)


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
