import sys
from typing import Iterable, Sequence
from functools import reduce
from bisect import bisect_right


def parse_input(input_: Iterable[str]) -> Iterable[Sequence[int]]:
    return (tuple(map(int, line.strip())) for line in input_)


def part1(input_: Iterable[str]) -> int:

    def joltage(bank: Sequence[int]) -> int:
        x1 = x2 = -1
        for index, jolt in enumerate(bank):
            if jolt > x1 and index != len(bank) - 1:
                x1, x2 = jolt, -1
            elif jolt > x2:
                x2 = jolt
        return x1 * 10 + x2

    return sum(map(joltage, parse_input(input_)))


def part2(input_: Iterable[str]) -> int:

    def joltage(bank: Sequence[int]) -> int:
        seq = []
        for index, jolt in enumerate(bank):
            seq_index = bisect_right(seq, -jolt, max(0, index - (len(bank) - 12)))
            if seq_index < 12:
                seq[seq_index:] = [-jolt]
        return reduce((lambda a, b: a*10 - b), seq, 0)

    return sum(map(joltage, parse_input(input_)))


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
