import sys
from typing import Iterable, Tuple, Sequence
from itertools import takewhile, chain, accumulate
import re
from bisect import bisect


def parse_input(input_: Iterable[str]) -> Tuple[Iterable[Tuple[int, int]], Iterable[int]]:
    rows = map(str.strip, input_)
    ranges = ((int(m.group(1)), int(m.group(2))) for m in (re.match('(\d+)-(\d+)', row) for row in takewhile(bool, rows)))
    return ranges, (int(row.strip()) for row in rows)


def flatten_ranges(ranges: Iterable[Tuple[int, int]]) -> Tuple[Sequence[int], Sequence[int]]:
    flat_ranges, deltas = zip(*sorted(chain.from_iterable(((start, 1), (end + 1, -1)) for start, end in ranges), key=lambda r: (r[0], -r[1])))
    return flat_ranges, tuple(accumulate(deltas))


def part1(input_: Iterable[str]) -> int:
    ranges, vals = parse_input(input_)
    flat_ranges, counts = flatten_ranges(ranges)

    def test_val(val: int) -> bool:
        i = bisect(flat_ranges, val)
        return i > 0 and counts[i - 1] > 0

    return sum(map(test_val, vals))


def part2(input_: Iterable[str]) -> int:
    ranges, _ = parse_input(input_)

    total = 0
    open_bound = None

    for (bound, count) in zip(*flatten_ranges(ranges)):
        if count == 0:
            total += bound - open_bound
            open_bound = None
        elif open_bound is None:
            open_bound = bound

    return total


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
