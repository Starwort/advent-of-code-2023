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

raw = aoc_helper.fetch(11, 2023)


def parse_raw(raw: str):
    return Grid.from_string(raw)


data = parse_raw(raw)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    empty_cols = set()
    empty_rows = set()
    for y, row in enumerate(data.data):
        if row.count(1) == 0:
            empty_rows.add(y)
    for col in range(data[0].len()):
        if all(row[col] == 0 for row in data.data):
            empty_cols.add(col)
    new_grid = Grid[int](
        list(
            list(0 for x in range(data.data[0].len() + len(empty_cols)))
            for y in range(data.data.len() + len(empty_rows))
        )
    )
    real_y = 0
    for y, row in enumerate(data.data):
        if y in empty_rows:
            real_y += 2
            continue
        real_x = 0
        for x, cell in enumerate(row):
            if x in empty_cols:
                real_x += 2
                continue
            new_grid[real_y][real_x] = cell
            real_x += 1
        real_y += 1
    all_points = set()
    for y, row in enumerate(new_grid.data):
        for x, cell in enumerate(row):
            if cell == 1:
                all_points.add((x, y))
    dist = 0
    for start, dest in itertools.combinations(all_points, 2):
        dist += abs(start[0] - dest[0]) + abs(start[1] - dest[1])
    return dist


aoc_helper.lazy_test(day=11, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    empty_cols = set()
    empty_rows = set()
    for y, row in enumerate(data.data):
        if row.count(1) == 0:
            empty_rows.add(y)
    for col in range(data[0].len()):
        if all(row[col] == 0 for row in data.data):
            empty_cols.add(col)
    all_points = set()
    for y, row in enumerate(data.data):
        for x, cell in enumerate(row):
            if cell == 1:
                all_points.add((x, y))
    dist = 0
    for start, dest in itertools.combinations(all_points, 2):
        dist += (
            abs(start[0] - dest[0])
            + abs(start[1] - dest[1])
            + 999999
            * (
                len(
                    [
                        empty
                        for empty in empty_cols
                        if min(start[0], dest[0]) < empty < max(start[0], dest[0])
                    ]
                )
                + len(
                    [
                        empty
                        for empty in empty_rows
                        if min(start[1], dest[1]) < empty < max(start[1], dest[1])
                    ]
                )
            )
        )
    return dist


# aoc_helper.lazy_test(day=11, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=11, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=11, year=2023, solution=part_two, data=data)
