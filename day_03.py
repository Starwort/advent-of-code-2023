from collections import defaultdict, deque
import string
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

raw = aoc_helper.fetch(3, 2023)


def parse_raw(raw: str):
    return Grid.from_string(raw, classify=str)


data = parse_raw(raw)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    symbols = set(string.printable) - set(string.ascii_letters) - set("1234567890.")
    numbers = {}
    for y, row in data.data.enumerated():
        for x, cell in row.enumerated():
            if cell in symbols:
                neighbours = data.neighbours(x, y)
                for (x_, y_), cell in neighbours:
                    if cell not in "1234567890":
                        continue
                    while x_ > 0 and data[y_][x_ - 1] in "1234567890":
                        x_ -= 1
                    num_pos = (x_, y_)
                    number = ""
                    while x_ < len(data[0]) and data[y_][x_] in "1234567890":
                        number += data[y_][x_]
                        x_ += 1
                    numbers[num_pos] = int(number)
    return sum(numbers.values())


aoc_helper.lazy_test(
    day=3,
    year=2023,
    parse=parse_raw,
    solution=part_one,
    test_data=(
        """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""",
        4361,
    ),
)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    total = 0
    for y, row in data.data.enumerated():
        for x, cell in row.enumerated():
            if cell == "*":
                neighbours = data.neighbours(x, y)
                numbers = {}
                for (x_, y_), cell in neighbours:
                    if cell not in "1234567890":
                        continue
                    while x_ > 0 and data[y_][x_ - 1] in "1234567890":
                        x_ -= 1
                    num_pos = (x_, y_)
                    number = ""
                    while x_ < len(data[0]) and data[y_][x_] in "1234567890":
                        number += data[y_][x_]
                        x_ += 1
                    numbers[num_pos] = int(number)
                if len(numbers) == 2:
                    a, b = numbers.values()
                    total += a * b
    return total


aoc_helper.lazy_test(day=3, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=3, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=3, year=2023, solution=part_two, data=data)
