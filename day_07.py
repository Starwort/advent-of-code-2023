from collections import Counter, defaultdict, deque
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

raw = aoc_helper.fetch(7, 2023)


def parse_raw(raw: str):
    return (
        list(raw.splitlines())
        .mapped(str.split)
        .mapped(lambda i: (list(i[0]), int(i[1])))
    )


data = parse_raw(raw)


def strength(hand: list[str]):
    cards = Counter(hand)
    if len(cards) == 1:
        return 5, hand.mapped(lambda i: "23456789TJQKA".index(i))
    if len(cards) == 2:
        a, b = sorted(cards.values())
        if b == 4:
            return 4, hand.mapped(lambda i: "23456789TJQKA".index(i))
        if b == 3:
            return 3.5, hand.mapped(lambda i: "23456789TJQKA".index(i))
    if 3 in cards.values():
        return 3, hand.mapped(lambda i: "23456789TJQKA".index(i))
    pairs = Counter(cards.values())[2]
    if pairs == 2:
        return 2, hand.mapped(lambda i: "23456789TJQKA".index(i))
    if pairs == 1:
        return 1, hand.mapped(lambda i: "23456789TJQKA".index(i))
    return 0, hand.mapped(lambda i: "23456789TJQKA".index(i))


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    hands = data.deepcopy()
    hands.sort(key=lambda i: strength(i[0]))
    return hands.iter().enumerate(1).map(lambda i: i[0] * i[1][1]).sum()


aoc_helper.lazy_test(day=7, year=2023, parse=parse_raw, solution=part_one)


def strength2(hand: list[str]):
    hand_innate_strength = hand.mapped(lambda i: "J23456789TQKA".index(i))
    strongest_hand = strength(hand)[0]
    n_jacks = hand.count(item="J")
    for jack_replacement in "23456789TQKA":
        if jack_replacement not in hand:
            continue
        new_hand = hand.mapped(lambda i: jack_replacement if i == "J" else i)
        new_hand_strength = strength(new_hand)[0]
        if new_hand_strength > strongest_hand:
            strongest_hand = new_hand_strength
    return strongest_hand, hand_innate_strength


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    hands = data.deepcopy()
    hands.sort(key=lambda i: strength2(i[0]))
    return hands.iter().enumerate(1).map(lambda i: i[0] * i[1][1]).sum()


aoc_helper.lazy_test(day=7, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=7, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=7, year=2023, solution=part_two, data=data)
