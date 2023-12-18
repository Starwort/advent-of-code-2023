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

raw = aoc_helper.fetch(18, 2023)


def parse_raw(raw: str) -> list[tuple[tuple[int, int], int, tuple[int, int], int]]:
    return (
        list(raw.splitlines())
        .mapped(str.split)
        .starmapped(  # type: ignore
            lambda dir, n, col: (
                [(0, -1), (0, 1), (-1, 0), (1, 0)]["UDLR".index(dir)],  # type: ignore
                int(n),
                [(1, 0), (0, 1), (-1, 0), (0, -1)][int(col[-2])],
                int(col[2:-2], 16),
            )
        )
    )


data = parse_raw(raw)


def fill(grid: SparseGrid[bool], start: tuple[int, int]) -> int:
    seen = set()
    queue = deque([start])
    filled = 0
    while queue:
        x, y = queue.popleft()
        if (x, y) in seen:
            continue
        seen.add((x, y))
        if (x, y) in grid.data:
            continue
        filled += 1
        queue.extend((x + dx, y + dy) for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)])
    return filled


def shoelace(points: list[tuple[int, int]]) -> int:
    total_area = 0
    for p1, p2 in zip(points, points[1:] + points[:1]):
        total_area += p1[0] * p2[1] - p1[1] * p2[0]
    return abs(total_area // 2)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    x = y = int()
    points = list([(x, y)])
    total_walls = 0
    for (dx, dy), n, *_ in data:
        target = (x + dx * n, y + dy * n)
        total_walls += n
        points.append(target)
        x, y = target
    return shoelace(points) + total_walls // 2 + 1


aoc_helper.lazy_test(day=18, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    return part_one(data.starmapped(lambda a, b, c, d: (c, d, a, b)))


aoc_helper.lazy_test(day=18, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=18, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=18, year=2023, solution=part_two, data=data)
