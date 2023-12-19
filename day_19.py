from collections import Counter, defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass
from typing import TypedDict

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

raw = aoc_helper.fetch(19, 2023)


@dataclass
class Lt:
    var: str
    val: int


@dataclass
class Gt:
    var: str
    val: int


type Condition = Lt | Gt


@dataclass
class Reject:
    pass


@dataclass
class Accept:
    pass


@dataclass
class UseFlow:
    flow: str


type Outcome = Reject | Accept | UseFlow


def parse_workflow(raw: str):
    name, data = raw[:-1].split("{")
    rules = data.split(",")
    rules2: list[tuple[Condition, Outcome]] = list()
    default = Reject()
    for rule in rules:
        if ":" in rule:
            cond, flow = rule.split(":")
            var, op, *_ = cond
            val = extract_ints(cond)[0]
            if op == "<":
                cond2 = Lt(var, val)
            elif op == ">":
                cond2 = Gt(var, val)
            else:
                raise ValueError(f"unknown operator {op}")
            if flow == "R":
                flow2 = Reject()
            elif flow == "A":
                flow2 = Accept()
            else:
                flow2 = UseFlow(flow)
            rules2.append((cond2, flow2))
        else:
            if rule == "R":
                flow2 = Reject()
            elif rule == "A":
                flow2 = Accept()
            else:
                flow2 = UseFlow(rule)
            default = flow2

    return name, rules2, default


def parse_raw(
    raw: str,
) -> tuple[
    dict[str, tuple[list[tuple[Condition, Outcome]], Outcome]], list[dict[str, int]]
]:
    workflows, ratings = raw.split("\n\n")
    workflows2 = {
        k: (v1, v2) for k, v1, v2 in list(workflows.splitlines()).mapped(parse_workflow)
    }
    ratings2: list[dict[str, int]] = list(ratings.splitlines()).mapped(extract_ints).starmapped(lambda x, m, a, s: {"x": x, "m": m, "a": a, "s": s})  # type: ignore
    return workflows2, ratings2


data = parse_raw(raw)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(
    data: tuple[
        dict[str, tuple[list[tuple[Condition, Outcome]], Outcome]],
        list[dict[str, int]],
    ] = data
):
    workflows, ratings = data
    total = 0
    for rating in ratings:
        flow = UseFlow("in")
        while isinstance(flow, UseFlow):
            conditions, default = workflows[flow.flow]
            for when, next in conditions:
                match when:
                    case Lt(var, val) if rating[var] < val:
                        flow = next
                        break
                    case Gt(var, val) if rating[var] > val:
                        flow = next
                        break
                    case _:
                        pass
            else:
                flow = default
        match flow:
            case Accept():
                total += sum(rating.values())
            case _:
                pass
    return total


aoc_helper.lazy_test(day=19, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(
    data: tuple[
        dict[str, tuple[list[tuple[Condition, Outcome]], Outcome]],
        list[dict[str, int]],
    ] = data
):
    workflows, _ = data
    total = 0
    todo: list[tuple[dict[str, range | multirange], Outcome]] = list(
        [
            (
                {
                    "x": range(4000) + 1,
                    "m": range(4000) + 1,
                    "a": range(4000) + 1,
                    "s": range(4000) + 1,
                },
                UseFlow("in"),
            )
        ]
    )
    while todo:
        rating, workflow = todo.pop()
        if any(len(val) == 0 for val in rating.values()):
            continue
        match workflow:
            case Accept():
                total += (
                    len(rating["x"])
                    * len(rating["m"])
                    * len(rating["a"])
                    * len(rating["s"])
                )
            case Reject():
                pass
            case UseFlow(flow):
                conditions, default = workflows[flow]
                for when, next in conditions:
                    match when:
                        case Lt(var, val):
                            rating2 = deepcopy(rating)
                            rating2[var] = range(rating[var].start, val)
                            todo.append((rating2, next))
                            rating[var] -= rating2[var]
                        case Gt(var, val):
                            rating2 = deepcopy(rating)
                            rating2[var] = range(val + 1, rating[var].stop)
                            todo.append((rating2, next))
                            rating[var] -= rating2[var]
                        case _:
                            pass
                todo.append((rating, default))
    return total


aoc_helper.lazy_test(day=19, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=19, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=19, year=2023, solution=part_two, data=data)
