import sys
from bisect import bisect
from itertools import combinations, chain
from typing import Iterable, Tuple
import re
import random



def parse_input(input_: Iterable[str]) -> Iterable[Tuple[int, int]]:
    return ((int(x), int(y)) for x, y in (re.match(r'(\d+),(\d+)', line).groups() for line in input_))


def get_area(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)


def part1(input_: Iterable[str]) -> int:
    points = tuple(parse_input(input_))
    return max(get_area(p1, p2) for p1, p2 in combinations(points, 2))


def part2(input_: Iterable[str]) -> int:
    points = list(parse_input(input_))

    vertical_borders = []
    horizontal_borders = []

    for (x0, y0), (x1, y1) in zip(points, chain(points[1:], (points[0],))):
        if x0 == x1:
            vertical_borders.append((x0, tuple(sorted((y0, y1)))))
        else:
            horizontal_borders.append((y0, tuple(sorted((x0, x1)))))

    vertical_borders.sort()
    horizontal_borders.sort()

    vertical_x = [v[0] for v in vertical_borders]
    horizontal_y = [h[0] for h in horizontal_borders]

    def overlaps_border(p1: Tuple[int, int], p2: Tuple[int, int]) -> bool:
        xr, yr = map(sorted, zip(p1, p2))

        for x0, (y0, y1) in vertical_borders[bisect(vertical_x, xr[0]):]:
            if x0 >= xr[1]:
                break
            if y1 > yr[0] and yr[1] > y0:
                return True
        for y0, (x0, x1) in horizontal_borders[bisect(horizontal_y, yr[0]):]:
            if y0 >= yr[1]:
                break
            if x1 > xr[0] and xr[1] > x0:
                return True
        return False

    max_area = 0
    random.shuffle(points)

    for p1, p2 in combinations(points, 2):
        area = get_area(p1, p2)
        if area > max_area and not overlaps_border(p1, p2):
            max_area = area
    return max_area


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))