from collections import Counter, defaultdict, deque
from math import prod

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
from networkx import Graph, connected_components, minimum_edge_cut

raw = aoc_helper.fetch(25, 2023)


def parse_raw(raw: str):
    connections = defaultdict(set)
    for k, vs in (
        list(raw.splitlines())
        .mapped(lambda s: s.split(": "))
        .starmapped(lambda k, vs: (k, set(vs.split())))
    ):
        connections[k] |= vs
        for v in vs:
            connections[v] |= {k}
    graph = Graph()
    graph.add_nodes_from(connections)
    graph.add_edges_from((k, v) for k, vs in connections.items() for v in vs)
    return graph


data = parse_raw(raw)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    edges = minimum_edge_cut(data)
    data.remove_edges_from(edges)
    a, b = connected_components(data)
    return len(a) * len(b)


# aoc_helper.lazy_test(day=25, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    ...


aoc_helper.lazy_submit(day=25, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=25, year=2023, solution=part_two, data=data)
