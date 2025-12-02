import sys
import re
from typing import Iterable
from itertools import accumulate, tee


def parse_input(input_: Iterable[str]) -> Iterable[int]:
    return ([-1, 1][dir_ == 'R'] * int(clicks) for dir_, clicks in (re.match(r'([LR])(\d+)', line).groups() for line in input_))


def part1(input_: Iterable[str]) -> int:
    return sum(val % 100 == 0 for val in accumulate(parse_input(input_), initial=50))


def part2(input_: Iterable[str]) -> int:
    rots1, rots2 = tee(parse_input(input_), 2)
    positions = accumulate(rots1, lambda pos, clicks: (pos + clicks) % 100, initial=50)
    return sum(abs(p := pos + clicks) // 100 + (pos != 0 and p <= 0) for pos, clicks in zip(positions, rots2))


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
