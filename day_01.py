from collections import defaultdict, deque
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

raw = aoc_helper.fetch(1, 2023)


def calibration(el):
    a = el[0]
    b = el[-1]
    a = int(str(a)[0])
    b %= 10
    return a * 10 + b


def parse_raw(raw: str):
    # return (
    #     list(raw.splitlines())
    #     .mapped(
    #         lambda i: i.replace("one", "1")
    #         .replace("eleven", "1")
    #         .replace("twelve", "2")
    #         .replace("thirteen", "3")
    #         .replace("fourteen", "4")
    #         .replace("fifteen", "5")
    #         .replace("sixteen", "6")
    #         .replace("seventeen", "7")
    #         .replace("eighteen", "8")
    #         .replace("nineteen", "9")
    #         .replace("ten", "10")
    #         .replace("two", "2")
    #         .replace("three", "3")
    #         .replace("four", "4")
    #         .replace("five", "5")
    #         .replace("six", "6")
    #         .replace("seven", "7")
    #         .replace("eight", "8")
    #         .replace("nine", "9")
    #         .replace("zero", "0")
    #     )
    #     .mapped(lambda line: fir(extract_ints(line)))
    # )
    return raw


data = parse_raw(raw)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    # the timeout of 1 minute is almost certainly going to be up by the time I
    # write a correct solution :P

    # that, or this happens to be the right answer (unlikely)
    return (
        list(data.splitlines())
        .mapped(lambda line: calibration(extract_ints(line)))
        .sum()
    )


aoc_helper.lazy_test(day=1, year=2023, parse=parse_raw, solution=part_one)


def first_dig(num: str):
    cands = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "0": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "zero": 0,
        "eleven": 1,
        "twelve": 1,
        "thirteen": 1,
        "fourteen": 1,
        "fifteen": 1,
        "sixteen": 1,
        "seventeen": 1,
        "eighteen": 1,
        "nineteen": 1,
    }
    first = 1000, 0
    for cand in cands:
        index = num.find(cand)
        if index != -1:
            if index < first[0]:
                first = index, cands[cand]
    return first[1]


def last_dig(num: str):
    cands = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "0": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "zero": 0,
        "eleven": 1,
        "twelve": 2,
        "thirteen": 3,
        "fourteen": 4,
        "fifteen": 5,
        "sixteen": 6,
        "seventeen": 7,
        "eighteen": 8,
        "nineteen": 9,
    }
    last = -1, 0
    for cand in cands:
        index = num.rfind(cand)
        if index != -1:
            if index > last[0]:
                last = index, cands[cand]
    return last[1]


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    lines = data.splitlines()
    nums = [first_dig(line) * 10 + last_dig(line) for line in lines]
    return sum(nums)


aoc_helper.lazy_test(day=1, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=1, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=1, year=2023, solution=part_two, data=data)
