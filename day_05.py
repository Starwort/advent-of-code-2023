import builtins
from collections import defaultdict, deque
from itertools import count
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

raw = aoc_helper.fetch(5, 2023)


class Table:
    def __init__(self, raw: str):
        self.ranges = []
        for dest, src, len in extract_ints(raw).chunked(3):
            self.ranges.append((src, dest, len))

    def __getitem__(self, key: int):
        for src, dest, len in self.ranges:
            if src <= key < src + len:
                return dest + key - src
        return key

    def reverse_lookup(self, key: int):
        for src, dest, len in self.ranges:
            if dest <= key < dest + len:
                return src + key - dest
        return key


def parse_raw(raw: str):
    seeds, *maps = raw.split("\n\n")
    seeds = extract_ints(seeds)
    out_maps: dict[str, tuple[str, Table]] = {}
    for map in maps:
        title, *_ = map.splitlines()
        from_, to = title.removesuffix(" map:").split("-to-")
        map_data = Table(map)
        out_maps[to] = (from_, map_data)
    return seeds, out_maps


data: tuple[list[int], dict[str, tuple[str, Table]]] = parse_raw(raw)


def look_up(maps: dict[str, tuple[str, Table]], seed: int):
    soil = maps["soil"][1][seed]
    fertiliser = maps["fertilizer"][1][soil]
    water = maps["water"][1][fertiliser]
    light = maps["light"][1][water]
    temp = maps["temperature"][1][light]
    humid = maps["humidity"][1][temp]
    loc = maps["location"][1][humid]
    return loc


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data: tuple[list[int], dict[str, tuple[str, Table]]] = data):
    seeds, maps = data
    locs = seeds.mapped(lambda seed: look_up(maps, seed))
    return locs.min()


aoc_helper.lazy_test(day=5, year=2023, parse=parse_raw, solution=part_one)


def reverse_lookup(maps: dict[str, tuple[str, Table]], loc: int):
    humid = maps["location"][1].reverse_lookup(loc)
    temp = maps["humidity"][1].reverse_lookup(humid)
    light = maps["temperature"][1].reverse_lookup(temp)
    water = maps["light"][1].reverse_lookup(light)
    fertiliser = maps["water"][1].reverse_lookup(water)
    soil = maps["fertilizer"][1].reverse_lookup(fertiliser)
    seed = maps["soil"][1].reverse_lookup(soil)
    return seed


def intersect_ranges(ranges: builtins.list[builtins.range], map: Table):
    out_ranges: builtins.list[builtins.range] = []
    for range in ranges:
        splits = [range]
        for src, dest, len in map.ranges:
            next_splits = []
            for split in splits:
                if split.start < src and split.stop < src:
                    next_splits.append(split)
                elif split.start < src and split.stop < src + len:
                    next_splits.append(builtins.range(split.start, src))
                    out_ranges.append(builtins.range(dest, split.stop - src + dest))
                elif split.start < src and split.stop >= src + len:
                    next_splits.append(builtins.range(split.start, src))
                    out_ranges.append(builtins.range(dest, dest + len))
                    next_splits.append(builtins.range(src + len, split.stop))
                elif split.start < src + len and split.stop < src + len:
                    out_ranges.append(
                        builtins.range(
                            split.start - src + dest, split.stop - src + dest
                        )
                    )
                elif split.start < src + len and split.stop >= src + len:
                    out_ranges.append(
                        builtins.range(split.start - src + dest, dest + len)
                    )
                    next_splits.append(builtins.range(src + len, split.stop))
                else:
                    next_splits.append(split)
            splits = next_splits
        out_ranges.extend(splits)
    return simplify_ranges(out_ranges)


def simplify_ranges(ranges: builtins.list[builtins.range]):
    if not ranges:
        return []
    ranges.sort(key=lambda range: range.start)
    last_range = ranges[0]
    out_ranges = [last_range]
    for range in ranges:
        if range.start == range.stop:
            continue
        if range.start <= last_range.stop:
            last_range = builtins.range(
                last_range.start, max(range.stop, last_range.stop)
            )
            out_ranges[-1] = last_range
        else:
            last_range = range
            out_ranges.append(last_range)
    return out_ranges


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data: tuple[list[int], dict[str, tuple[str, Table]]] = data):
    seeds, maps = data
    in_ranges = [
        *seeds.chunked(2).mapped(lambda pair: builtins.range(pair[0], sum(pair)))
    ]
    soils = intersect_ranges(in_ranges, maps["soil"][1])
    fertilisers = intersect_ranges(soils, maps["fertilizer"][1])
    waters = intersect_ranges(fertilisers, maps["water"][1])
    lights = intersect_ranges(waters, maps["light"][1])
    temps = intersect_ranges(lights, maps["temperature"][1])
    humids = intersect_ranges(temps, maps["humidity"][1])
    locs = intersect_ranges(humids, maps["location"][1])
    return min(loc.start for loc in locs)


aoc_helper.lazy_test(day=5, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=5, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=5, year=2023, solution=part_two, data=data)
