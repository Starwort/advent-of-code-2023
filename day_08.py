from collections import defaultdict, deque, Counter
import itertools

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

raw = aoc_helper.fetch(8, 2023)


def parse_raw(raw: str):
    first, rest = raw.split("\n\n")
    return first, {
        a: (b, c)
        for a, b, c in list(rest.splitlines()).mapped(
            lambda i: i.replace(" =", "")
            .replace("(", "")
            .replace(")", "")
            .replace(",", "")
            .split()
        )
    }


data: tuple[str, dict[str, tuple[str, str]]] = parse_raw(raw)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data: tuple[str, dict[str, tuple[str, str]]] = data):
    here = "AAA"
    directions, info = data
    for i, direction in enumerate(itertools.cycle(directions), 1):
        here = info[here][direction == "R"]
        if here == "ZZZ":
            return i


# aoc_helper.lazy_test(day=8, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data: tuple[str, dict[str, tuple[str, str]]] = data):
    directions, info = data
    locations = [i for i in info if i.endswith("A")]
    times = []
    for here in locations:
        for i, direction in enumerate(itertools.cycle(directions), 1):
            here = info[here][direction == "R"]
            if here.endswith("Z"):
                times.append(i)
                break
    from math import lcm

    return lcm(*times)
    # cycle_starts = [-1 for i in locations]
    # cycle_ends = [-1 for i in locations]
    # seen = [{(i, int()): 0} for i in locations]
    # for i, direction in enumerate(itertools.cycle(directions), 1):
    #     locations = [info[location][direction == "R"] for location in locations]
    #     for j, location in enumerate(locations):
    #         if location in seen[j]:
    #             if cycle_starts[j] == -1:
    #                 cycle_starts[j] = seen[j][location, i % len(directions)]
    #                 cycle_ends[j] = i
    #         else:
    #             seen[j][location, i % len(directions)] = i
    #     if all(i != -1 for i in cycle_starts):
    #         # if any(len([k for k,v in seen[j].items() if k.endswith('Z') and v >= cycle_start[j]]) > 1 for j, _ in enumerate(locations)):
    #         #     print(i, cycle_start, cycle_end, locations, seen)
    #         #     return
    #         zs = [
    #             [
    #                 v
    #                 for k, v in seen[j].items()
    #                 if k[0].endswith("Z") and v >= cycle_starts[0]
    #             ]
    #             for j, _ in enumerate(locations)
    #         ]
    #         min_timestep = min(min(i) for i in zs)
    #         while True:
    #             for i, (part_zs, cycle_start, cycle_end) in enumerate(
    #                 zip(zs, cycle_starts, cycle_ends)
    #             ):
    #                 min_timestep = max(min(part_zs), min_timestep)
    #                 new_zs = [
    #                     v + (cycle_end - cycle_start if v < min_timestep else 0)
    #                     for v in part_zs
    #                 ]
    #                 zs[i] = new_zs
    #             if all(min_timestep in i for i in zs):
    #                 return min_timestep
    #     if all(i.endswith("Z") for i in locations):
    #         return i


aoc_helper.lazy_test(day=8, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=8, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=8, year=2023, solution=part_two, data=data)
