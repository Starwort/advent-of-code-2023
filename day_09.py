from collections import defaultdict, deque, Counter

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
    range,
    multirange,
    search,
    tail_call,
)

raw = aoc_helper.fetch(9, 2023)


def parse_raw(raw: str):
    return list(raw.splitlines()).mapped(extract_ints)


data = parse_raw(raw)


def history(row: list[int]) -> int:
    diffs = row.windowed(2).starmapped(lambda a, b: b - a)
    if all(i == 0 for i in diffs):
        return row[-1]
    else:
        return row[-1] + history(diffs)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    total = 0
    for row in data:
        total += history(row)
    return total


aoc_helper.lazy_test(day=9, year=2023, parse=parse_raw, solution=part_one)


def history2(row: list[int]) -> int:
    diffs = row.windowed(2).starmapped(lambda a, b: b - a)
    if all(i == 0 for i in diffs):
        return row[0]
    else:
        return row[0] - history2(diffs)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    total = 0
    for row in data:
        total += history2(row)
    return total


aoc_helper.lazy_test(day=9, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=9, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=9, year=2023, solution=part_two, data=data)
