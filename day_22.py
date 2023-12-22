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

raw = aoc_helper.fetch(22, 2023)


def parse_raw(raw: str):
    return extract_ints(raw).chunked(3).chunked(2)


data = parse_raw(raw)

assert data.all(lambda brick: brick[0][2] <= brick[1][2])


def fall(data=data):
    new_data = data.copy()
    new_data.sort(key=lambda brick: brick[0][2])  # sort by ascending z
    heights = defaultdict(lambda: (int(), int(-1)))
    load_bearing = set()
    graph = list([list() for _ in new_data])
    for i, brick in new_data.enumerated():
        (sx, sy, sz), (ex, ey, ez) = brick
        min_brick_height = max(
            heights[x, y][0] for x in irange(sx, ex) for y in irange(sy, ey)
        )
        this_rests_on = {
            heights[x, y][1]
            for x in irange(sx, ex)
            for y in irange(sy, ey)
            if heights[x, y][0] == min_brick_height and heights[x, y][1] != -1
        }
        if len(this_rests_on) == 1:
            load_bearing.update(this_rests_on)
        for resting_on in this_rests_on:
            graph[resting_on].append(i)
        new_sz = min_brick_height + 1
        assert ez >= sz
        new_ez = new_sz + ez - sz
        new_data[i] = brick = (sx, sy, new_sz), (ex, ey, new_ez)
        for x in irange(sx, ex):
            for y in irange(sy, ey):
                heights[x, y] = new_ez, i
    return new_data, load_bearing, graph


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    # min_z = 1
    settled, load_bearing, _ = fall(data)
    # print(load_bearing)
    # total = 0
    # for disintegrate in range(len(settled)):
    #     tmp = settled[:disintegrate] + settled[disintegrate + 1 :]
    #     assert settled != tmp, (disintegrate, settled)
    #     fell = fall(tmp)[0]
    #     if fell == tmp:
    #         total += 1
    # return total
    return len(settled) - len(load_bearing)
    # total = 0
    # for i, brick in settled.enumerated():
    #     tmp = settled.filtered(lambda b: b != brick)
    #     if fall(tmp) == tmp:
    #         total += 1
    # return total


aoc_helper.lazy_test(day=22, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    _, _, graph = fall(data)

    def count(idx: int, graph: list[list[int]]):
        table = [0 for _ in data]
        for j in range(len(data)):
            for i in graph[j]:
                table[i] += 1
        todo = [idx]
        count = -1
        while len(todo) > 0:
            count += 1
            x = todo.pop()
            for i in graph[x]:
                table[i] -= 1
                if table[i] == 0:
                    todo.append(i)
        return count

    return sum(count(i, graph) for i in range(len(data)))


aoc_helper.lazy_test(day=22, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=22, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=22, year=2023, solution=part_two, data=data)
