import sys
from typing import Iterable, Tuple
import re
from math import log, ceil
from itertools import takewhile


def parse_input(input_: Iterable[str]) -> Iterable[Tuple[int, int]]:
    ranges_str = re.findall(r'(\d+)-(\d+),?', next(iter(input_)))
    return ((int(start), int(end)) for start, end in ranges_str)


def gen_repeated(start_prefix: int) -> Iterable[int]:
    prefix = start_prefix
    while True:
        yield prefix * 10 ** (int(log(prefix, 10) + .0000001) + 1) + prefix
        prefix += 1


def gen_repeated_times(start_prefix: int, times: int) -> Iterable[int]:
    pattern = re.compile(r'^(\d+)\1+$')
    end_prefix = 10 ** (int(log(start_prefix, 10)) + 1)
    for prefix in map(str, range(start_prefix, end_prefix)):
        if pattern.match(prefix) is None:
            yield int(prefix * times)


def part1(input_: Iterable[str]) -> int:

    def sum_repeated(start: int, end: int) -> int:
        n_digits = int(log(start, 10)) + 1
        start_prefix = start // (10 ** (n_digits // 2)) if n_digits %2 == 0 else 10 ** (n_digits // 2)
        return sum((start <= value) * value for value in takewhile(lambda v: v <= end, gen_repeated(start_prefix)))

    return sum(sum_repeated(start, end) for start, end in parse_input(input_))


def part2(input_: Iterable[str]) -> int:

    def sum_repeated(start: int, end: int) -> int:
        total = 0
        s_start = str(start)
        s_end = str(end)
        for length in range(1, len(s_end) // 2 + 1):
            rtimes_start = max(2, int(ceil(len(s_start) / length)))
            rtimes_end = len(s_end) // length
            for repeat_times in range(rtimes_start, rtimes_end + 1):
                start_prefix = int(s_start[:length]) if repeat_times * length == len(s_start) else int(10 ** (length - 1))
                total += sum((start <= value <= end) * value for value in takewhile(lambda v: v <= end, gen_repeated_times(start_prefix, repeat_times)))
        return total

    return sum(sum_repeated(start, end) for start, end in parse_input(input_))


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
