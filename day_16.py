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

raw = aoc_helper.fetch(16, 2023)


def parse_raw(raw: str):
    return Grid.from_string(raw, str)


data = parse_raw(raw)


def laser(data: Grid[str], x: int, y: int, dx: int, dy: int):
    beams = deque([(x, y, dx, dy)])
    energised = {(x, y)}
    explored = set()
    while beams:
        x, y, dx, dy = beams.popleft()
        if (x, y, dx, dy) in explored:
            continue
        explored.add((x, y, dx, dy))
        while y in range(len(data.data)) and x in range(len(data[y])):
            energised.add((x, y))
            if data[y][x] != ".":
                break
            x += dx
            y += dy
        else:
            continue
        if data[y][x] == "/":
            dx, dy = -dy, -dx
            beams.append((x + dx, y + dy, dx, dy))
        elif data[y][x] == "\\":
            dx, dy = dy, dx
            beams.append((x + dx, y + dy, dx, dy))
        elif data[y][x] == "|" and dx != 0:
            beams.append((x, y + 1, 0, 1))
            beams.append((x, y - 1, 0, -1))
        elif data[y][x] == "-" and dy != 0:
            beams.append((x + 1, y, 1, 0))
            beams.append((x - 1, y, -1, 0))
        else:
            beams.append((x + dx, y + dy, dx, dy))
    return len(energised)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    return laser(data, 0, 0, 1, 0)


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
