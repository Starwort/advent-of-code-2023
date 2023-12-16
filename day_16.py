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

raw = aoc_helper.fetch(16, 2023)


def parse_raw(raw: str):
    return Grid.from_string(raw, str)


data = parse_raw(raw)


def laser(data: Grid[str], x: int, y: int, dx: int, dy: int):
    beams = [(x, y, dx, dy)]
    energised = Grid[bool](list(list(False for _ in row) for row in data.data))
    explored = set()
    while beams:
        next_beams = []
        for x, y, dx, dy in beams:
            if (x, y, dx, dy) in explored:
                continue
            explored.add((x, y, dx, dy))
            if not (y in range(len(data.data)) and x in range(len(data[y]))):
                continue
            energised[y][x] = True
            if data[y][x] == "/":
                dx, dy = -dy, -dx
                next_beams.append((x + dx, y + dy, dx, dy))
            elif data[y][x] == "\\":
                dx, dy = dy, dx
                next_beams.append((x + dx, y + dy, dx, dy))
            elif data[y][x] == "|" and dx != 0:
                next_beams.append((x, y + 1, 0, 1))
                next_beams.append((x, y - 1, 0, -1))
            elif data[y][x] == "-" and dy != 0:
                next_beams.append((x + 1, y, 1, 0))
                next_beams.append((x - 1, y, -1, 0))
            else:
                next_beams.append((x + dx, y + dy, dx, dy))
        beams = next_beams
    return energised.data.mapped(sum).sum()


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    beams = [(0, 0, 1, 0)]
    energised = Grid[bool](list(list(False for _ in row) for row in data.data))
    explored = set()
    while beams:
        next_beams = []
        for x, y, dx, dy in beams:
            if (x, y, dx, dy) in explored:
                continue
            explored.add((x, y, dx, dy))
            if not (y in range(len(data.data)) and x in range(len(data[y]))):
                continue
            energised[y][x] = True
            if data[y][x] == "/":
                dx, dy = -dy, -dx
                next_beams.append((x + dx, y + dy, dx, dy))
            elif data[y][x] == "\\":
                dx, dy = dy, dx
                next_beams.append((x + dx, y + dy, dx, dy))
            elif data[y][x] == "|" and dx != 0:
                next_beams.append((x, y + 1, 0, 1))
                next_beams.append((x, y - 1, 0, -1))
            elif data[y][x] == "-" and dy != 0:
                next_beams.append((x + 1, y, 1, 0))
                next_beams.append((x - 1, y, -1, 0))
            else:
                next_beams.append((x + dx, y + dy, dx, dy))
        beams = next_beams
    return energised.data.mapped(sum).sum()


aoc_helper.lazy_test(day=16, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    return max(
        max(laser(data, x, 0, 0, 1) for x in range(len(data[0]))),
        max(laser(data, 0, y, 1, 0) for y in range(len(data.data))),
        max(laser(data, x, len(data.data) - 1, 0, -1) for x in range(len(data[0]))),
        max(laser(data, len(data[0]) - 1, y, -1, 0) for y in range(len(data.data))),
    )


aoc_helper.lazy_test(day=16, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=16, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=16, year=2023, solution=part_two, data=data)
