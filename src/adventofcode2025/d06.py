import sys
from itertools import zip_longest, groupby
from typing import Iterable, Sequence, Tuple
import re
from operator import add, mul
from functools import reduce


def parse_input1(input_: Iterable[str]) -> Tuple[Sequence[str], Iterable[Iterable[int]]]:
    *vals, ops = (line.strip().split() for line in input_)
    return ops, (map(int, row) for row in vals)


def parse_input2(input_: Iterable[str]) -> Tuple[Sequence[str], Iterable[Iterable[int]]]:
    *vals, ops = (line.strip('\n') for line in input_)
    return ops.split(), ((int(''.join(col)) for col in char_col) for is_break, char_col in groupby(zip_longest(*vals, fillvalue=' '), key=lambda c: all(v == ' ' for v in c)) if not is_break)


def part1(input_: Iterable[str]) -> int:
    ops, vals = parse_input1(input_)
    return sum(reduce([add, mul][op == '*'], col) for op, col in zip(ops, zip(*vals)))


def part2(input_: Iterable[str]) -> int:
    ops, vals = parse_input2(input_)
    return sum(reduce([add, mul][op == '*'], col) for op, col in zip(ops, vals))


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))