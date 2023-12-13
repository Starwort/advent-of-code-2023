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

raw = aoc_helper.fetch(13, 2023)


def parse_raw(raw: str):
    return list(raw.split("\n\n")).mapped(Grid.from_string)


data = parse_raw(raw)


def reflect_x(grid: Grid, mirror_x: int) -> list[int]:
    reflect_range = min(mirror_x, grid[0].len() - mirror_x)
    return grid.data.mapped(
        lambda row: sum(
            a != b
            for a, b in zip(
                row[mirror_x - reflect_range : mirror_x],
                row[mirror_x : mirror_x + reflect_range][::-1],
            )
        )
    )


def reflect_y(grid: Grid, mirror_y: int) -> list[int]:
    reflect_range = min(mirror_y, grid.data.len() - mirror_y)
    return list(
        sum(a != b for a, b in zip(a, b))
        for a, b in zip(
            grid.data[mirror_y - reflect_range : mirror_y],
            grid.data[mirror_y : mirror_y + reflect_range][::-1],
        )
    )


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    total = 0
    for i, grid in data.enumerated():
        for mirror_x in range(grid[0].len()):
            if reflect_x(grid, mirror_x).sum() == 0:
                total += mirror_x
        for mirror_y in range(grid.data.len()):
            if reflect_y(grid, mirror_y).sum() == 0:
                total += 100 * mirror_y
    return total


aoc_helper.lazy_test(day=13, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    total = 0
    for i, grid in data.enumerated():
        for mirror_x in range(grid[0].len()):
            if reflect_x(grid, mirror_x).sum() == 1:
                total += mirror_x
        for mirror_y in range(grid.data.len()):
            if reflect_y(grid, mirror_y).sum() == 1:
                total += 100 * mirror_y
    return total


aoc_helper.lazy_test(day=13, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=13, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=13, year=2023, solution=part_two, data=data)
