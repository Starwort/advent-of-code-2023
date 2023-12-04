from collections import defaultdict, deque
from typing import TYPE_CHECKING

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
    search,
    tail_call,
)

raw = aoc_helper.fetch(4, 2023)


def parse_raw(raw: str):
    return (
        list(raw.splitlines())
        .mapped(lambda line: line.split(": ")[1].split(" | "))
        .mapped_each(extract_ints)
    )


data = parse_raw(raw)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    points = 0
    for card in data:
        winning, have = card
        winning = set[int](winning)
        have = set[int](have)
        have_winning = winning & have
        if len(have_winning) != 0:
            points += 2 ** (len(have_winning) - 1)
    return points


aoc_helper.lazy_test(day=4, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    copies = [1 for _ in data]
    for i, (card, n_copies) in enumerate(zip(data, copies)):
        winning, have = card
        winning = set[int](winning)
        have = set[int](have)
        have_winning = winning & have
        for card in range(i + 1, len(have_winning) + i + 1):
            copies[card] += n_copies
    return sum(copies)


aoc_helper.lazy_test(day=4, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=4, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=4, year=2023, solution=part_two, data=data)
