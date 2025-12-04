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
import re

INPUTS_DIR = 'inputs'
TEST_INPUTS_DIR = 'test_inputs'


def create_solution() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--day', type=int)
    args = parser.parse_args()
    day = args.day

    for input_dir in (INPUTS_DIR, TEST_INPUTS_DIR):
        if not os.path.exists(input_dir):
            os.mkdir(input_dir)

    script_path = os.path.join(os.path.dirname(adventofcode2025.__file__), f'{pad_day(day)}.py')
    input_paths = [get_input_path(input_dir, day) for input_dir in (INPUTS_DIR, TEST_INPUTS_DIR)]
    if any(os.path.exists(path) for path in (script_path, *input_paths)):
        raise RuntimeError(f'Files already created for day {day}')

    for path in input_paths:
        with open(path, 'w') as _:
            pass

    shutil.copy(solution_template.__file__, script_path)


def profile_solution() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--day', type=int)
    parser.add_argument('--samples', type=int, default=5)
    parser.add_argument('--part', type=int, choices=[1, 2])
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()

    day = args.day
    part = args.part
    samples = args.samples
    test = args.test

    solution = get_solution(day, part)
    input_ = read_input(day, test)
    with cProfile.Profile() as pr:
        for _ in range(samples):
            solution(input_)
    pr.print_stats(-1)


def run_solutions() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', nargs='*', type=int)
    parser.add_argument('--samples', type=int, default=5)
    parser.add_argument('--parts', type=int, nargs='+', choices=[1, 2], default=[1, 2])
    parser.add_argument('--test', action='store_true')

    args = parser.parse_args()

    days = args.days or all_days()
    samples = args.samples
    parts = args.parts
    test = args.test

    print(tabulate.tabulate(
        [(f'Day {day} - Part {part}', result, runtime) for day in days for part, result, runtime in run_day_solution(day, samples, parts, test)],
        ['Problem', 'Result', f'Runtime ({samples} samples)'],
    ))


def update_runtimes():
    parser = argparse.ArgumentParser()
    parser.add_argument('--samples', type=int, default=5)

    args = parser.parse_args()
    samples = args.samples

    header = ['Day', f'Part 1 Runtime ({samples} samples)', f'Part 2 Runtime ({samples} samples)']
    runtimes = []

    part1_total = part2_total = 0
    for day in all_days():
        (_, _, part1_time), (_, _, part2_time) = run_day_solution(day, samples, [1, 2], False)
        runtimes.append([day, part1_time, part2_time])
        part1_total += part1_time
        part2_total += part2_time
    runtimes.append(['Total', part1_total, part2_total])
    with open('README.md', 'w') as fi:
        fi.write('''
# Solution Runtimes
*on my machine

''')
        fi.write(tabulate.tabulate(runtimes, header, 'pipe'))


def pad_day(day: int) -> str:
    return 'd' + f'0{day}'[-2:]


def get_input_path(input_dir: str, day: int) -> str:
    return f'{input_dir}/{pad_day(day)}.txt'


def read_input(day: int, test: bool) -> Iterable[str]:
    input_dir = TEST_INPUTS_DIR if test else INPUTS_DIR
    with open(get_input_path(input_dir, day), 'r') as fi:
        return tuple(fi)


def get_solution(day: int, part: int) -> Callable[[Iterable[str]], int]:
    s = importlib.import_module(f'adventofcode2025.{pad_day(day)}')
    if part == 1:
        return s.part1
    elif part == 2:
        return s.part2
    raise RuntimeError(f'No solution for day {day} - part {part}')


def run_day_solution(day: int, samples: int, parts: Sequence[int], test: bool) -> Iterable[Tuple[int, Optional[int], float]]:

    def time_function(f: Callable[[], int]) -> Tuple[Optional[int], float]:
        class Wrapped:
            def __call__(self):
                self.response = f()

        wrapped = Wrapped()

        runtime = timeit(wrapped, number=samples) / samples
        return wrapped.response, runtime
    input_ = read_input(day, test)

    for part in parts:
        solution = get_solution(day, part)
        result, time = time_function(lambda: solution(input_))
        yield part, result, time


def all_days() -> Iterable[int]:
    solution_dir = os.path.dirname(adventofcode2025.__file__)
    return sorted(int(match.group(1)) for file in os.listdir(solution_dir) if (match := re.match(r'd0*(\d+).py', file)) is not None)
