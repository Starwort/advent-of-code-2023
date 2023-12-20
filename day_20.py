from collections import Counter, defaultdict, deque
from itertools import count
from math import lcm
from typing import Callable, Literal

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

raw = aoc_helper.fetch(20, 2023)


def parse_module(raw: str):
    name, params = raw.split(" -> ")
    params = params.split(", ")
    match name[0]:
        case "%":
            mode = "%"
            name = name[1:]
        case "&":
            mode = "&"
            name = name[1:]
        case _:
            mode = ""
    return name, mode, list(params)


def parse_raw(raw: str) -> dict[str, tuple[Literal["%", "&", ""], list[str]]]:
    modules = list(raw.splitlines())
    return {name: (mode, params) for name, mode, params in modules.mapped(parse_module)}


data: dict[str, tuple[Literal["%", "&", ""], list[str]]] = parse_raw(raw)


def handle(
    states: dict[str, bool],
    remembered: dict[str, dict[str, bool]],
    data: dict[str, tuple[Literal["%", "&", ""], list[str]]],
    on_activate: Callable[[str, bool, str], None] = lambda mod, pulse, origin: None,
) -> tuple[int, int]:
    modules = data["broadcaster"][1]
    queue = deque((mod, bool(), str("broadcaster")) for mod in modules)
    high = 0
    low = 0
    while queue:
        name, pulse, origin = queue.popleft()
        # print(origin + f" -" + ("high" if pulse else "low") + f"-> {name}")
        on_activate(name, pulse, origin)
        if pulse:
            high += 1
        else:
            low += 1
        if name not in data:
            continue
        mode, params = data[name]
        match mode:
            case "%":
                if not pulse:
                    states[name] = not states[name]
                    queue.extend((mod, states[name], name) for mod in params)
            case "&":
                remembered[name][origin] = pulse
                pulse = not all(remembered[name].values())
                queue.extend((mod, pulse, name) for mod in params)
            case "":
                queue.extend((mod, pulse, name) for mod in params)
    return high, low


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data: dict[str, tuple[Literal["%", "&", ""], list[str]]] = data):
    states = {name: False for name, (mode, _) in data.items() if mode == "%"}
    remembered = {
        name: {input: False for input, (_, params) in data.items() if name in params}
        for name, (mode, params) in data.items()
        if mode == "&"
    }
    results = {}
    total_high = 0
    total_low = 0
    for i in range(1000):
        # frozen = (
        #     tuple(states.items()),
        #     tuple((k, tuple(v.items())) for k, v in remembered.items()),
        # )
        # if frozen in results:
        #     # found cycle
        #     cycle_start, *_ = results[frozen]
        #     cycle_length = i - cycle_start
        #     cycle_total = sum(
        #         low * high for j, high, low in results.values() if j >= cycle_start
        #     )
        #     cycle_total *= (1000 - cycle_start) // cycle_length
        #     cycle_total += sum(
        #         low * high for j, high, low in results.values() if j < cycle_start
        #     )
        #     return cycle_total

        high, low = handle(states, remembered, data)
        total_high += high
        total_low += low + 1
        # results[frozen] = i, high, low
    print(total_high, total_low)
    return total_high * total_low


aoc_helper.lazy_test(
    day=20,
    year=2023,
    parse=parse_raw,
    solution=part_one,
    test_data=(
        """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""",
        32000000,
    ),
)
aoc_helper.lazy_test(
    day=20,
    year=2023,
    parse=parse_raw,
    solution=part_one,
    test_data=(
        """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""",
        11687500,
    ),
)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
# def part_two(data: dict[str, tuple[Literal["%", "&", ""], list[str]]] = data):
#     states = {name: False for name, (mode, _) in data.items() if mode == "%"}
#     remembered = {
#         name: {input: False for input, (_, params) in data.items() if name in params}
#         for name, (mode, params) in data.items()
#         if mode == "&"
#     }
#     result = []
#     for i in count(1):

#         def on_activate(mod: str, pulse: bool, origin: str):
#             if mod == "dr" and pulse:
#                 print(f"{i}: {origin} -" + ("high" if pulse else "low") + f"-> dr")
#             if mod == "rx":
#                 # print(f"{i}: {origin} -" + ("high" if pulse else "low") + f"-> rx")
#                 if not pulse:
#                     result.append(i)


#         handle(states, remembered, data, on_activate)
#         if result:
#             return result[0]
def part_two(data: dict[str, tuple[Literal["%", "&", ""], list[str]]] = data):
    states = {name: False for name, (mode, _) in data.items() if mode == "%"}
    remembered = {
        name: {input: False for input, (_, params) in data.items() if name in params}
        for name, (mode, params) in data.items()
        if mode == "&"
    }
    assert iter(data.values()).filter(lambda dat: "rx" in dat[1]).count() == 1
    source = next(name for name, (_, params) in data.items() if "rx" in params)
    assert data[source][0] == "&"
    sources = list(remembered[source].keys())
    assert sources.all(lambda source: data[source][0] == "&")

    cycles = {}
    for i in count(1):
        if i % 10_000 == 0:
            print(i)

        def on_activate(mod: str, pulse: bool, origin: str):
            if mod in sources and not pulse and mod not in cycles:
                print(f"{i}: {origin} -low-> {mod}")
                cycles[mod] = i

        handle(states, remembered, data, on_activate)

        if len(cycles) == len(sources):
            return lcm(*cycles.values())


aoc_helper.lazy_submit(day=20, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=20, year=2023, solution=part_two, data=data)
