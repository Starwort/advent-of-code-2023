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

raw = aoc_helper.fetch(10, 2023)


def parse_raw(raw: str):
    lines = list(raw.splitlines())
    start_ = lines.enumerated().find(lambda i: i[1].find("S") != -1)
    assert start_ is not None
    start: tuple[int, int] = start_[1].index("S"), start_[0]
    x, y = start

    def classify(cell: str) -> tuple[bool, bool, bool, bool]:
        match cell:
            case ".":
                return (False, False, False, False)
            case "|":
                return (True, False, True, False)
            case "-":
                return (False, True, False, True)
            case "L":
                return (True, True, False, False)
            case "J":
                return (True, False, False, True)
            case "7":
                return (False, False, True, True)
            case "F":
                return (False, True, True, False)
            case "S":
                up = y > 0 and classify(lines[y - 1][x])[2]
                left = x > 0 and classify(lines[y][x - 1])[1]
                down = y < len(lines) - 1 and classify(lines[y + 1][x])[0]
                right = x < len(lines[0]) - 1 and classify(lines[y][x + 1])[3]
                return (up, right, down, left)
            case _:
                return (False, False, False, False)

    grid = Grid.from_string(raw, classify)

    return start, grid


def unclassify(cell: tuple[bool, bool, bool, bool]) -> str:
    return {
        (bool(), bool(), bool(), bool()): ".",
        (True, False, True, False): "|",
        (False, True, False, True): "-",
        (True, True, False, False): "L",
        (True, False, False, True): "J",
        (False, False, True, True): "7",
        (False, True, True, False): "F",
        (True, True, True, True): "S",
    }[cell]


data: tuple[tuple[int, int], Grid[tuple[bool, bool, bool, bool]]] = parse_raw(raw)


def explore(
    grid: Grid[tuple[bool, bool, bool, bool]], start: tuple[int, int]
) -> dict[tuple[int, int], int]:
    to_search = deque[tuple[int, int, int]]([start + (0,)])
    seen = {}
    while to_search:
        x, y, dist = to_search.popleft()
        if (x, y) in seen:
            continue
        seen[x, y] = dist
        up, right, down, left = grid[y][x]
        if up:
            to_search.append((x, y - 1, dist + 1))
        if right:
            to_search.append((x + 1, y, dist + 1))
        if down:
            to_search.append((x, y + 1, dist + 1))
        if left:
            to_search.append((x - 1, y, dist + 1))
    return seen


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data: tuple[tuple[int, int], Grid[tuple[bool, bool, bool, bool]]] = data):
    start, grid = data
    seen = explore(grid, start)
    return max(seen.values())


aoc_helper.lazy_test(day=10, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data: tuple[tuple[int, int], Grid[tuple[bool, bool, bool, bool]]] = data):
    start, grid = data
    big_grid = SparseGrid(bool)
    for x, y in explore(grid, start):
        up, right, down, left = grid[y][x]
        x *= 2
        y *= 2
        big_grid[x, y] = True
        if up:
            big_grid[x, y - 1] = True
        if right:
            big_grid[x + 1, y] = True
        if down:
            big_grid[x, y + 1] = True
        if left:
            big_grid[x - 1, y] = True

    def flood_fill(x, y):
        area = 0
        to_search = deque([(x, y)])
        seen = set()
        while to_search:
            x, y = to_search.popleft()
            if (x, y) in seen:
                continue
            seen.add((x, y))
            if x % 2 == 0 and y % 2 == 0:
                area += 1
                if area > grid.data.len() * grid[0].len():
                    return
            for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                if (
                    x + dx < 0
                    or y + dy < 0
                    or x + dx >= grid[0].len() * 2
                    or y + dy >= grid.data.len() * 2
                ):
                    return
                if not big_grid[x + dx, y + dy]:
                    to_search.append((x + dx, y + dy))
        return area

    x, y = start

    for ox, oy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        area = flood_fill(2 * x + ox, 2 * y + oy)
        if area is not None:
            return area
    raise RuntimeError("couldn't find area")


for test_data in [
    (
        """...........
.F-------7.
.SF-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""",
        4,
    ),
    (
        """..........
.F------7.
.SF----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........""",
        4,
    ),
    (
        """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJF7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7S.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""",
        8,
    ),
    (
        """FF7F7F7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7SL7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""",
        10,
    ),
]:
    aoc_helper.lazy_test(
        day=10,
        year=2023,
        parse=parse_raw,
        solution=part_two,
        test_data=test_data,
    )

aoc_helper.lazy_submit(day=10, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=10, year=2023, solution=part_two, data=data)
