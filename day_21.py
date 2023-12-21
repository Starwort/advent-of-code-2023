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

raw = aoc_helper.fetch(21, 2023)


def parse_raw(raw: str):
    start = list(raw.splitlines()).enumerated().find(lambda i: "S" in i[1])
    assert start is not None
    sy = start[0]
    sx = start[1].index("S")
    return (sx, sy), Grid.from_string(raw, lambda i: ".S#".index(i) // 2)


data = parse_raw(raw)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    start, grid = data
    grid: Grid[int]
    found_after_64 = set()
    seen = set()
    todo = deque([(start, int())])
    while todo:
        pos, dist = todo.popleft()
        if (pos, dist) in seen:
            continue
        seen.add((pos, dist))
        if dist == 64:
            found_after_64.add(pos)
            continue
        for npos, nval in grid.orthogonal_neighbours(*pos):
            if nval == 1:
                continue
            todo.append((npos, dist + 1))
    return len(found_after_64)


# aoc_helper.lazy_test(day=21, year=2023, parse=parse_raw, solution=part_one)


def mk_even_odd(
    start: tuple[int, int], grid: Grid[int]
) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    even = set()
    odd = set()

    seen = set()
    todo = deque([(start, int())])
    while todo:
        pos, dist = todo.popleft()
        if pos in seen:
            continue
        seen.add(pos)
        if dist % 2 == 0:
            even.add(pos)
        else:
            odd.add(pos)
        for npos, nval in grid.orthogonal_neighbours(*pos):
            if nval == 1:
                continue
            todo.append((npos, dist + 1))

    return even, odd


def explore(target: int, data=data):
    start, grid = data
    grid: Grid[int]
    seen = set()
    todo = deque([(start, int())])
    total = 0
    w = len(grid[0])
    h = len(grid.data)
    while todo:
        pos, dist = todo.popleft()
        if pos in seen:
            continue
        total += dist % 2 == target % 2
        seen.add(pos)
        if dist == target:
            continue
        x, y = pos
        for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx = x + ox
            ny = y + oy
            if grid[ny % h][nx % w] == 1:
                continue
            todo.append(((nx, ny), dist + 1))
    return total


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data, target=26501365):
    start, grid = data
    grid: Grid[int]
    w = len(grid[0])
    h = len(grid.data)

    assert w == h == 131
    assert start == (65, 65)

    assert grid[start[1]].none()
    assert grid.transpose()[start[0]].none()

    # it's quadratic for some reason??
    # there's probably a deeply mathematical reason for this
    # but I'm not smart enough to figure it out
    a0 = explore(65, data)
    a1 = explore(65 + 131, data)
    a2 = explore(65 + 131 * 2, data)

    b0, b1, b2 = a0, a1 - a0, a2 - a1
    n = (target - 65) // 131
    return b0 + b1 * n + (n * (n - 1) // 2) * (b2 - b1)

    even, odd = mk_even_odd(start, grid)

    possible_even = len(even)
    possible_odd = len(odd)

    print("even", possible_even, "odd", possible_odd)

    # there aren't any obstacles in the same row or column as the start
    # so we can just flood fill from the start to the borders
    explored_grids = {(int(), int())}
    todo = PrioQueue[tuple[int, int, int]](
        [(0, -1, h), (0, 1, h), (-1, 0, w), (1, 0, w)]
    )
    fill_todo = deque[tuple[int, int, int, int, int]]([])
    for gx, gy, dist in todo:
        if (gx, gy) in explored_grids:
            continue
        explored_grids.add((gx, gy))
        if dist % 2 == 0:
            possible_even += len(even)
        else:
            possible_odd += len(odd)
        if dist + w < target:
            todo.push((gx - 1, gy, dist + w))
            todo.push((gx + 1, gy, dist + w))
        else:
            fill_todo.append((w - 1, 0, gx - 1, gy, dist + w - 1 - start[0]))
            fill_todo.append((0, 0, gx + 1, gy, dist + start[0]))
        if dist + h < target:
            todo.push((gx, gy - 1, dist + h))
            todo.push((gx, gy + 1, dist + h))
        else:
            fill_todo.append((0, h - 1, gx, gy - 1, dist + h - 1 - start[1]))
            fill_todo.append((0, 0, gx, gy + 1, dist + start[1]))
    print("after exploring by grids", possible_even, possible_odd)
    seen = set()
    for x, y, gx, gy, dist in fill_todo:
        if (gx, gy) in explored_grids or (x, y, gx, gy, dist) in seen:
            continue
        seen.add((x, y, gx, gy, dist))
        if dist > target:
            continue
        print(len(fill_todo), len(seen))
        if dist % 2 == 0:
            possible_even += 1
        else:
            possible_odd += 1
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = (x + dx, y + dy)
            ngx, ngy = gx, gy
            if nx < 0:
                ngx -= 1
            elif nx >= w:
                ngx += 1
            nx %= w
            if ny < 0:
                ngy -= 1
            elif ny >= h:
                ngy += 1
            ny %= h
            fill_todo.append((nx, ny, ngx, ngy, dist + 1))
    print("after filling", possible_even, possible_odd)

    return possible_even if target % 2 == 0 else possible_odd


aoc_helper.lazy_submit(day=21, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=21, year=2023, solution=part_two, data=data)
