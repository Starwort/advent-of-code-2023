from collections import Counter, defaultdict, deque
from functools import cache
from itertools import permutations, product

import aoc_helper
from aoc_helper import (  # search,
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
    tail_call,
)

raw = aoc_helper.fetch(12, 2023)


def parse_raw(raw: str):
    return (
        list(raw.splitlines())
        .mapped(str.split)
        .starmapped(
            lambda record, nums: (
                list[int](".#?".index(c) for c in record),
                extract_ints(nums),
            )
        )
    )


data = parse_raw(raw)


def runs(data: list[int], nums: list[int]) -> bool:
    nums_iter = iter(nums)
    run = 0
    for val in data:
        if val == 1:
            run += 1
        elif val == 0 and run != 0:
            if run != next(nums_iter, -1):
                return False
            run = 0
    if run != 0 and run != next(nums_iter, -1):
        return False
    run = 0
    return next(nums_iter, -1) == -1


def get_runs(data: list[int]) -> list[int]:
    runs = list()
    run = 0
    for val in data:
        if val == 1:
            run += 1
        elif val == 0 and run != 0:
            runs.append(run)
            run = 0
        elif val == 2:
            return runs
    if run != 0:
        runs.append(run)
    return runs


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    total = 0
    for record, nums in data:
        to_replace = record.count(2)
        necessary_sum = sum(nums) - record.count(1)
        total += search(tuple(record), None, tuple(nums))
    return total


aoc_helper.lazy_test(day=12, year=2023, parse=parse_raw, solution=part_one)


# def search(data: list[int], nums: list[int]) -> int:
#     try:
#         next_to_replace = data.index(2)
#     except Exception:
#         if get_runs(data) == nums:
#             return 1
#         return 0
#     total = 0
#     for val in range(2):
#         data[next_to_replace] = val
#         runs = get_runs(data)
#         if len(runs) > len(nums) or runs and runs[-1] != nums[len(runs) - 1]:
#             # if any(a != b for a, b in zip(runs, nums)):
#             continue
#         total += search(data, nums)
#     data[next_to_replace] = 2
#     return total


# def search(data: list[int], nums: list[int]) -> int:
#     try:
#         next_to_replace = data.index(2)
#     except Exception:
#         if get_runs(data) == nums:
#             return 1
#         return 0
#     runs = get_runs(data)
#     runs_left = nums[len(runs) :]
#     if not runs_left:
#         return runs == nums
#     next_run = runs_left[0]
#     data[next_to_replace] = 0
#     total = search(data, nums)
#     data[next_to_replace] = 2
#     original = data[next_to_replace : next_to_replace + next_run]
#     if 0 in original or len(original) != next_run:
#         return 0
#     for i in range(next_run):
#         data[next_to_replace + i] = 1
#     total += search(data, nums)
#     data[next_to_replace : next_to_replace + next_run] = original
#     return total


@cache
def search(data: tuple[int], in_run: int, remain: tuple[int]) -> int:
    if not data:
        if in_run is None and len(remain) == 0:
            return 1
        if len(remain) == 1 and in_run is not None and in_run == remain[0]:
            return 1
        return 0
    possibilities = 0
    for ch in data:
        if ch != 0:
            possibilities += 1
    if in_run is not None and possibilities + in_run < sum(remain):
        return 0
    if in_run is None and possibilities < sum(remain):
        return 0
    if in_run is not None and len(remain) == 0:
        return 0
    poss = 0
    if data[0] == 0 and in_run is not None and in_run != remain[0]:
        return 0
    if data[0] == 0 and in_run is not None:
        poss += search(data[1:], None, remain[1:])
    if data[0] == 2 and in_run is not None and in_run == remain[0]:
        poss += search(data[1:], None, remain[1:])
    if (data[0] == 1 or data[0] == 2) and in_run is not None:
        poss += search(data[1:], in_run + 1, remain)
    if (data[0] == 2 or data[0] == 1) and in_run is None:
        poss += search(data[1:], 1, remain)
    if (data[0] == 2 or data[0] == 0) and in_run is None:
        poss += search(data[1:], None, remain)
    return poss


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    total = 0
    for i, (record, nums) in data.enumerated():
        nums = tuple(nums)
        # # optimise for the fast case
        # if all(i == 1 for i in record[-nums[-1] :]):
        #     total += search(tuple(record), None, nums) ** 5
        #     continue
        this_row = search(tuple((record + [2]) * 4 + record), None, nums * 5)
        # print(i, record, nums, this_row)
        total += this_row
    return total


aoc_helper.lazy_test(
    day=12,
    year=2023,
    parse=parse_raw,
    solution=part_two,
    test_data=(
        """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""",
        525152,
    ),
)

aoc_helper.lazy_submit(day=12, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=12, year=2023, solution=part_two, data=data)
