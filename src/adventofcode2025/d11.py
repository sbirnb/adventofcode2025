import sys
from collections import defaultdict
from typing import Iterable, Mapping, Collection


def parse_input(input_: Iterable[str]) -> Mapping[str, Collection[str]]:
    return {k: tuple(v.split()) for k, v in (line.strip().split(': ') for line in input_)}


def part1(input_: Iterable[str]) -> int:
    edges = parse_input(input_)
    total = 0
    path_counts = defaultdict(int)
    path_counts['you'] = 1
    while path_counts:
        next_path_counts = defaultdict(int)
        for tail, count in path_counts.items():
            for extend in edges[tail]:
                if extend == 'out':
                    total += count
                else:
                    next_path_counts[extend] += count
        path_counts = next_path_counts
    return total


def part2(input_: Iterable[str]) -> int:
    edges = parse_input(input_)
    total = 0
    path_counts = defaultdict(int)
    path_counts['svr', False, False] = 1
    while path_counts:
        next_path_counts = defaultdict(int)
        for (tail, has_dac, has_fft), count in path_counts.items():
            for extend in edges[tail]:
                if extend == 'out':
                    if has_dac and has_fft:
                        total += count
                else:
                    next_path_counts[extend, has_dac or extend == 'dac', has_fft or extend == 'fft'] += count
        path_counts = next_path_counts
    return total


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))