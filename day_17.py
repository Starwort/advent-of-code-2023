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

raw = aoc_helper.fetch(17, 2023)


def parse_raw(raw: str):
    return Grid.from_string(raw)


data = parse_raw(raw)


def pathfind(
    grid: "Grid[int]",
    heuristic_multiplier: float = 1,
    min_rx: int = 0,
    max_rx: int = 3,
) -> None | int:
    to_visit = PrioQueue([(int(), int(), (int(), int()), int(), int(), [])])
    visited = set()
    target = len(grid.data[0]) - 1, len(grid.data) - 1

    heuristic = lambda x, y: abs(x - target[0]) + abs(y - target[1])

    for _heuristic_cost, cost, (x, y), rx, ry, history in to_visit:
        if (
            (x, y) == target
            and (rx == 0 or abs(rx) >= min_rx)
            and (ry == 0 or abs(ry) >= min_rx)
        ):
            display = Grid(list(list(str(i) for i in row) for row in grid.data))
            for x, y, rx, ry in history:
                display[y][x] = (
                    ">" if rx > 0 else "<" if rx < 0 else "^" if ry < 0 else "v"
                )
            print(display)
            return cost
        if (x, y, rx, ry) in visited:
            continue
        visited.add((x, y, rx, ry))
        for neighbour, value in grid.orthogonal_neighbours(x, y):
            if rx != 0 and rx < min_rx and rx > -min_rx:
                # must continue in the same direction
                if neighbour[0] == x:
                    continue
            if ry != 0 and ry < min_rx and ry > -min_rx:
                if neighbour[1] == y:
                    continue
            # if neighbour x > x, rx must be positive or 0 and also less than 3
            # if neighbour x < x, rx must be negative or 0 and also greater than -3
            # if neighbour y > y, ry must be positive or 0 and also less than 3
            # if neighbour y < y, ry must be negative or 0 and also greater than -3
            if (
                (neighbour[0] > x and (rx >= max_rx or rx < 0))
                or (neighbour[0] < x and (rx <= -max_rx or rx > 0))
                or (neighbour[1] > y and (ry >= max_rx or ry < 0))
                or (neighbour[1] < y and (ry <= -max_rx or ry > 0))
            ):
                continue
            next_cost = cost + value
            new_rx = (rx + neighbour[0] - x) if neighbour[0] != x else 0
            new_ry = (ry + neighbour[1] - y) if neighbour[1] != y else 0
            to_visit.push(
                (
                    next_cost + heuristic(*neighbour) * heuristic_multiplier,
                    next_cost,
                    neighbour,
                    # increment rx if was an x move, otherwise reset to 0
                    new_rx,
                    # increment ry if was a y move, otherwise reset to 0
                    new_ry,
                    [*history, (*neighbour, new_rx, new_ry)],
                )
            )


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    return pathfind(data)


aoc_helper.lazy_test(day=17, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    return pathfind(data, min_rx=4, max_rx=10)


aoc_helper.lazy_test(
    day=17,
    year=2023,
    parse=parse_raw,
    solution=part_two,
    test_data=(
        """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""",
        94,
    ),
)
aoc_helper.lazy_test(
    day=17,
    year=2023,
    parse=parse_raw,
    solution=part_two,
    test_data=(
        """111111111111
999999999991
999999999991
999999999991
999999999991""",
        71,
    ),
)

aoc_helper.lazy_submit(day=17, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=17, year=2023, solution=part_two, data=data)
