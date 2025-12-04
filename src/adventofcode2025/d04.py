import sys
from typing import Iterable, Sequence, Set


ADJACENT = (1j, -1j, 1, -1, 1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j)


def parse_input(input_: Iterable[str]) -> Iterable[complex]:
    return (row + column * 1j for row, columns in enumerate(input_) for column, value in enumerate(columns) if value == '@')


def part1(input_: Iterable[str]) -> int:
    rolls = set(parse_input(input_))

    def check_roll(roll: complex) -> bool:
        return sum(roll + d in rolls for d in ADJACENT) < 4

    return sum(map(check_roll, rolls))


def part2(input_: Iterable[str]) -> int:
    adjacent_counts = {roll: 0 for roll in parse_input(input_)}

    for roll in adjacent_counts:
        adjacent_counts[roll] = sum(roll + d in adjacent_counts for d in ADJACENT)

    def remove_rolls():
        remove_queue = [roll for roll, adjacent in adjacent_counts.items() if adjacent < 4]
        while remove_queue:
            roll = remove_queue.pop()
            yield roll
            for adjacent_roll in (r for d in ADJACENT if (r := roll + d) in adjacent_counts):
                adjacent_counts[adjacent_roll] -= 1
                if adjacent_counts[adjacent_roll] == 3:
                    remove_queue.append(adjacent_roll)

    return sum(1 for _ in remove_rolls())


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))