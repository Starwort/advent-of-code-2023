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


def next_state(min_rx: int = 0, max_rx: int = 3):
    def next_state(
        state: tuple[int, int], dx: int, dy: int, _prev_cell: int, _new_cell: int
    ):
        rx, ry = state
        if (
            (0 < rx < max_rx and dx < 0)
            or (-max_rx < rx < 0 and dx > 0)
            or (abs(rx) == max_rx and dx != 0)
            or (0 < ry < max_rx and dy < 0)
            or (-max_rx < ry < 0 and dy > 0)
            or (abs(ry) == max_rx and dy != 0)
            or (rx != 0 and abs(rx) < min_rx and dx == 0)
            or (ry != 0 and abs(ry) < min_rx and dy == 0)
        ):
            return None
        return (rx * dx + dx, ry * dy + dy)

    return next_state


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    return data.pathfind(
        initial_state=(0, 0), next_state=next_state(), cost_function=lambda _, j: j
    )


aoc_helper.lazy_test(day=17, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_two(data=data):
    return data.pathfind(
        initial_state=(0, 0),
        next_state=next_state(4, 10),
        is_valid_end=lambda state: (abs(state[0]) >= 4 or state[0] == 0)
        and (abs(state[1]) >= 4 or state[1] == 0),
        cost_function=lambda _, j: j,
    )


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
