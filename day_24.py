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

raw = aoc_helper.fetch(24, 2023)


def parse_raw(raw: str):
    return extract_ints(raw).chunked(3).chunked(2)


data = parse_raw(raw)
import math


def line_intersection(
    line1: tuple[float, float, float, float], line2: tuple[float, float, float, float]
):
    x1, x2, x3, x4 = line1[0], line1[2], line2[0], line2[2]
    y1, y2, y3, y4 = line1[1], line1[3], line2[1], line2[3]

    dx1 = x2 - x1
    dx2 = x4 - x3
    dy1 = y2 - y1
    dy2 = y4 - y3
    dx3 = x1 - x3
    dy3 = y1 - y3

    det = dx1 * dy2 - dx2 * dy1
    det1 = dx1 * dy3 - dx3 * dy1
    det2 = dx2 * dy3 - dx3 * dy2

    if det == 0.0:  # lines are parallel
        if det1 != 0.0 or det2 != 0.0:  # lines are not co-linear
            return None  # so no solution

        if dx1:
            if x1 < x3 < x2 or x1 > x3 > x2:
                return math.inf  # infinitely many solutions
        else:
            if y1 < y3 < y2 or y1 > y3 > y2:
                return math.inf  # infinitely many solutions

        if line1[0] == line2[0] or line1[1] == line2[0]:
            return line2[0]
        elif line1[0] == line2[1] or line1[1] == line2[1]:
            return line2[1]

        return None  # no intersection

    s = det1 / det
    t = det2 / det

    if 0.0 < s < 1.0 and 0.0 < t < 1.0:
        return x1 + t * dx1, y1 + t * dy1


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data, test_start=200000000000000, test_end=400000000000000):
    total = 0
    for i, ((x1, y1, _), (vx1, vy1, _)) in data.enumerated():
        for (x2, y2, _), (vx2, vy2, _) in data[i + 1 :]:
            # project the line into the area test_start <= x <= test_end
            # and test_start <= y <= test_end
            # x1 + vx1 * t1 = test_start
            if (
                (vx1 == 0 and not (test_start <= x1 <= test_end))
                or (vx2 == 0 and not (test_start <= x2 <= test_end))
                or (vy1 == 0 and not (test_start <= y1 <= test_end))
                or (vy2 == 0 and not (test_start <= y2 <= test_end))
            ):
                continue
            t1 = (test_start - x1) / vx1
            t2 = (test_start - x2) / vx2
            t3 = (test_end - x1) / vx1
            t4 = (test_end - x2) / vx2
            lines = (
                (x1 + vx1 * t1, y1 + vy1 * t1, x1 + vx1 * t3, y1 + vy1 * t3),
                (x2 + vx2 * t2, y2 + vy2 * t2, x2 + vx2 * t4, y2 + vy2 * t4),
            )
            # determine line intersection
            match line_intersection(lines[0], lines[1]):
                case None:
                    continue
                case math.inf:
                    # lines are colinear
                    # confirm that lines pass through the correct y
                    # if 200000000000000 <= y1 + vy1 * (t2 + t4) / 2 <= 400000000000000:
                    #     total += 1
                    raise NotImplementedError()
                case (x, y):
                    # lines intersect
                    if vx1 != 0:
                        t1 = (x - x1) / vx1
                    else:
                        t1 = (y - y1) / vy1
                    if vx2 != 0:
                        t2 = (x - x2) / vx2
                    else:
                        t2 = (y - y2) / vy2
                    if t1 > 0 and t2 > 0 and test_start <= y <= test_end:
                        # print("intersection", x, y)
                        total += 1
    return total


p1test = part_one(
    parse_raw(
        """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
    ),
    7,
    27,
)
assert p1test == 2, p1test

# aoc_helper.lazy_test(day=24, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    from z3 import Int, Solver, sat

    x = Int("x")
    y = Int("y")
    z = Int("z")
    vx = Int("vx")
    vy = Int("vy")
    vz = Int("vz")
    ans = Int("ans")
    ts = [Int(f"t{i}") for i in range(len(data))]
    solver = Solver()
    for i, ((x1, y1, z1), (vx1, vy1, vz1)) in data.enumerated():
        solver.add(x1 + vx1 * ts[i] == x + vx * ts[i])
        solver.add(y1 + vy1 * ts[i] == y + vy * ts[i])
        solver.add(z1 + vz1 * ts[i] == z + vz * ts[i])
    solver.add(ans == x + y + z)
    if solver.check() != sat:
        print("oh god")
        return
    model = solver.model()
    return model[ans]


aoc_helper.lazy_test(day=24, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=24, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=24, year=2023, solution=part_two, data=data)
