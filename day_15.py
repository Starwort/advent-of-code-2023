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

raw = aoc_helper.fetch(15, 2023)


def parse_raw(raw: str):
    return raw.split(",")


def hash(data: str) -> int:
    val = 0
    for c in data:
        val += ord(c)
        val *= 17
        val %= 256
    return val


data = parse_raw(raw)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    return sum(map(hash, data))


aoc_helper.lazy_test(day=15, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    boxes = [{} for _ in range(256)]
    for instruction in data:
        if "=" in instruction:
            box, focal_length = instruction.split("=")
            boxes[hash(box)][box] = focal_length
        if "-" in instruction:
            box = instruction[:-1]
            boxes[hash(box)].pop(box, None)
    return sum(
        i * int(focal_length) * box
        for box, lens in enumerate(boxes, 1)
        for i, focal_length in enumerate(lens.values(), 1)
    )


aoc_helper.lazy_test(day=15, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=15, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=15, year=2023, solution=part_two, data=data)
