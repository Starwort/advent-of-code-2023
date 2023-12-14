import itertools
from collections import Counter, defaultdict, deque

import aoc_helper
from aoc_helper import (
    Grid,
    PrioQueue,
    SparseGrid,
    decode_text,
    extract_ints,
    extract_iranges,
    extract_ranges,
    extract_uints,
    frange,
    irange,
    iter,
    list,
    map,
    multirange,
    range,
    search,
    tail_call,
)

raw = aoc_helper.fetch(14, 2023)


def parse_raw(raw: str):
    return Grid.from_string(raw, classify=".O#".index)


data = parse_raw(raw)


def tilt_up(grid: Grid) -> Grid:
    return tilt_left(grid.transpose()).transpose()


def tilt_left(grid: Grid) -> Grid:
    return Grid(
        list(
            list(
                i
                for is_stationary, row in itertools.groupby(row, lambda i: i == 2)
                for i in (row if is_stationary else sorted(row, reverse=True))
            )
            for row in grid.data
        )
    )


def tilt_right(grid: Grid) -> Grid:
    return Grid(
        list(
            list(
                i
                for is_stationary, row in itertools.groupby(row, lambda i: i == 2)
                for i in (row if is_stationary else sorted(row))
            )
            for row in grid.data
        )
    )


def tilt_down(grid: Grid) -> Grid:
    return tilt_right(grid.transpose()).transpose()


def load(grid: Grid) -> int:
    load = 0
    found_rocks = 0
    for row in grid.data:
        for cell in row:
            if cell == 1:
                found_rocks += 1
        load += found_rocks
    return load


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    new_grid = tilt_up(data)
    return load(new_grid)


aoc_helper.lazy_test(day=14, year=2023, parse=parse_raw, solution=part_one)


def freeze(grid: Grid) -> str:
    return "\n".join("".join(".O#"[cell] for cell in row) for row in grid.data)


def cycle(grid: Grid) -> Grid:
    grid = tilt_up(grid)
    grid = tilt_left(grid)
    grid = tilt_down(grid)
    grid = tilt_right(grid)
    return grid


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    results = {freeze(data): 0}
    idx_to_grid = {0: data}
    cycle_result = data

    for i in range(1000000000) + 1:
        cycle_result = cycle(cycle_result)
        frozen = freeze(cycle_result)
        if frozen in results:
            cycle_start = results[frozen]
            cycle_length = i - cycle_start
            remaining = 1000000000 - cycle_start
            remaining %= cycle_length
            return load(idx_to_grid[remaining + cycle_start])
        else:
            results[frozen] = i
            idx_to_grid[i] = cycle_result


aoc_helper.lazy_test(day=14, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=14, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=14, year=2023, solution=part_two, data=data)
