import sys
from functools import reduce
from itertools import combinations
from typing import Iterable, Sequence, Tuple
import re
from operator import xor
import mip


def parse_input(input_: Iterable[str]) -> Iterable[Tuple[Sequence[bool], Sequence[Sequence[int]], Sequence[int]]]:
    return ((
        tuple(c == '#' for c in re.match(r'^\[([.#]+)', line).group(1)),
        tuple(tuple(map(int, s.split(','))) for s in re.findall(r'\(([\d,]+)\)', line)),
        tuple(map(int, re.search(r'\{([\d,]+)\}', line).group(1).split(',')))
    ) for line in input_)


def part1(input_: Iterable[str]) -> int:

    def n_switches(target: int, switches: Sequence[int]) -> int:
        return next(n for n in range(1, len(switches) + 1) if any(reduce(xor, c) == target for c in combinations(switches, n)))

    return sum(n_switches(
        reduce(lambda a, b: a << 1 | b, reversed(target), 0),
        tuple((reduce(lambda a, i: a | (1 << i), s, 0) for s in switches))
    ) for target, switches, _ in parse_input(input_))


def part2(input_: Iterable[str]) -> int:
    model = mip.Model()

    def n_switches(target: Sequence[int], switches: Sequence[Sequence[bool]]) -> int:
        model.clear()
        switch_vars = [model.add_var(f's_{i}', var_type=mip.INTEGER, lb=0, obj=1) for i in range(len(switches))]

        for i, (target_val, switch_vals) in enumerate(zip(target, zip(*switches))):
            model.add_constr(mip.xsum(var for s, var in zip(switch_vals, switch_vars) if s) == target_val)
        model.verbose=0
        model.optimize()
        return int(model.objective.x + .1)

    return sum(n_switches(
        target,
        tuple(tuple(a in switch for a in range(len(target))) for switch in switches)
    ) for _, switches, target in parse_input(input_))


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))