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
def part_one(data=data, scale=2):
    dist = 0
    points_captured = 0
    distance_travelled = 0
    for row in data.data:
        points_in_row = row.sum()
        dist += distance_travelled * points_in_row
        if points_in_row == 0:
            distance_travelled += scale * points_captured
        else:
            points_captured += points_in_row
            distance_travelled += points_captured
    points_captured = 0
    distance_travelled = 0
    for row in data.transpose().data:
        points_in_col = row.sum()
        dist += distance_travelled * points_in_col
        if points_in_col == 0:
            distance_travelled += scale * points_captured
        else:
            points_captured += points_in_col
            distance_travelled += points_captured
    return dist


aoc_helper.lazy_test(day=11, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    return part_one(data, 1_000_000)


# aoc_helper.lazy_test(day=11, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=11, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=11, year=2023, solution=part_two, data=data)
