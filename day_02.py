import builtins
from collections import defaultdict, deque
from math import prod
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

raw = aoc_helper.fetch(2, 2023)


def parse_game(parts: builtins.list[str]):
    return {part.split()[1]: int(part.split()[0]) for part in parts}


def parse_raw(raw: str):
    lines = list(raw.splitlines()).mapped(lambda line: line.split(": ")[1].split("; "))
    lines = lines.mapped_each(lambda line: parse_game(line.split(", ")))
    return lines


data = parse_raw(raw)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    sum = 0
    for id, game in data.enumerated(1):
        for round in game:
            if (
                round.get("blue", 0) > 14
                or round.get("red", 0) > 12
                or round.get("green", 0) > 13
            ):
                break
        else:
            sum += id
    return sum


aoc_helper.lazy_test(day=2, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    power = 0
    for id, game in data.enumerated(1):
        bag = {}
        for round in game:
            for colour, count in round.items():
                bag[colour] = max(bag.get(colour, 0), count)
        power += prod(bag.values())
    return power


aoc_helper.lazy_test(
    day=2,
    year=2023,
    parse=parse_raw,
    solution=part_two,
    test_data=(
        """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""",
        2286,
    ),
)

aoc_helper.lazy_submit(day=2, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=2, year=2023, solution=part_two, data=data)
