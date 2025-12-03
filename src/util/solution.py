# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

import argparse
import os
import shutil
import importlib
from timeit import timeit
from typing import Callable, Tuple, Sequence, Optional, Iterable
import tabulate
import util.solution_template as solution_template
import adventofcode2025
import cProfile


def pad_day(day: int) -> str:
    return 'd' + f'0{day}'[-2:]


def get_input_path(day: int) -> str:
    return f'inputs/{pad_day(day)}.txt'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', nargs='?', choices=['create', 'run', 'profile'])
    parser.add_argument('--days', nargs='*', type=int)
    parser.add_argument('--day', nargs='?', type=int)
    parser.add_argument('--samples', type=int, default=5)
    parser.add_argument('--parts', type=int, nargs='+', choices=[1, 2])
    parser.add_argument('--part', type=int, choices=[1, 2])

    return parser.parse_args()


def create_solution(day: int) -> None:
    inputs_path = get_input_path(day)
    script_path = os.path.join(os.path.dirname(adventofcode2025.__file__), f'{pad_day(day)}.py')
    if not os.path.exists('inputs'):
        os.mkdir('inputs')
    if os.path.exists(inputs_path) or os.path.exists(script_path):
        raise RuntimeError(f'Files already created for day {day}')
    with open(inputs_path, 'w') as _:
        pass
    shutil.copy(solution_template.__file__, script_path)


def read_input(day: int) -> Iterable[str]:
    with open(get_input_path(day), 'r') as fi:
        return tuple(fi)


def get_solution(day: int, part: int) -> Callable[[Iterable[str]], int]:
    s = importlib.import_module(f'adventofcode2025.{pad_day(day)}')
    if part == 1:
        return s.part1
    elif part == 2:
        return s.part2
    raise RuntimeError(f'No solution for day {day} - part {part}')


def profile_solution(day: int, part: int, samples: int) -> None:
    solution = get_solution(day, part)
    input_ = read_input(day)
    with cProfile.Profile() as pr:
        for _ in range(samples):
            solution(input_)
    pr.print_stats(-1)


def run_solutions(days: Iterable[int], parts: Sequence[int], samples: int) -> None:
    print(tabulate.tabulate(
        [(f'Day {day} - Part {part}', result, runtime) for day in days for part, result, runtime in run_day_solution(day, samples, parts)],
        headers=['Problem', 'Result', f'Runtime ({samples} samples)']
    ))


def run_day_solution(day: int, samples: int, parts: Sequence[int]) -> Iterable[Tuple[int, Optional[int], float]]:

    def time_function(f: Callable[[], int]) -> Tuple[Optional[int], float]:
        class Wrapped:
            def __call__(self):
                self.response = f()

        wrapped = Wrapped()

        runtime = timeit(wrapped, number=samples) / samples
        return wrapped.response, runtime

    input_ = read_input(day)

    for part in parts:
        solution = get_solution(day, part)
        result, time = time_function(lambda: solution(input_))
        yield part, result, time


def main() -> None:
    args = parse_args()
    if args.action == 'create':
        create_solution(args.day)
    elif args.action == 'run':
        run_solutions(args.days or [args.day], args.parts or [args.part], args.samples)
    elif args.action == 'profile':
        profile_solution(args.day, args.part, args.samples)
