from collections import Counter, defaultdict, deque
from time import perf_counter

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

raw = aoc_helper.fetch(23, 2023)


def parse_raw(raw: str):
    return Grid.from_string(raw, str)


data = parse_raw(raw)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    pos = (data[0].index("."), int())
    todo = PrioQueue([(int(), pos, frozenset())])
    best = 0
    for dist, (x, y), seen in todo:
        if y < 0:
            continue
        if (x, y) in seen:
            continue
        if y == len(data.data) - 1:
            best = max(best, -dist)
            continue
        match data[y][x]:
            case "#":
                continue
            case "<":
                todo.push((dist - 1, (x - 1, y), seen | {(x, y)}))
            case ">":
                todo.push((dist - 1, (x + 1, y), seen | {(x, y)}))
            case "^":
                todo.push((dist - 1, (x, y - 1), seen | {(x, y)}))
            case "v":
                todo.push((dist - 1, (x, y + 1), seen | {(x, y)}))
            case ".":
                for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
                    todo.push((dist - 1, (x + dx, y + dy), seen | {(x, y)}))
    assert best != 0
    return best


aoc_helper.lazy_test(day=23, year=2023, parse=parse_raw, solution=part_one)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
# def part_two(data=data):
#     pos = (data[0].index("."), int())
#     tx, ty = (data[-1].index("."), len(data.data) - 1)
#     todo = PrioQueue([(int(), int(), pos, frozenset())])
#     best = 0
#     for _heuristic, dist, (x, y), seen in todo:
#         if y < 0:
#             continue
#         if (x, y) in seen:
#             continue
#         if data[y][x] == "#":
#             continue
#         else:
#             PRUNE_VAL = 20
#             HEURISTIC_VAL = 10
#             if dist + (abs(x - tx) + abs(y - ty)) * PRUNE_VAL < best:
#                 # probably hopeless
#                 print(
#                     "skipping",
#                     dist,
#                     (x, y),
#                     # seen,
#                     "as best is",
#                     best,
#                     "and heuristic is",
#                     (abs(x - tx) + abs(y - ty)) * PRUNE_VAL,
#                 )
#                 continue
#             if y == len(data.data) - 1:
#                 best = max(best, dist)
#                 continue
#             for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
#                 todo.push(
#                     (
#                         -dist - 1 - (abs(x - tx) - abs(y - ty)) * HEURISTIC_VAL,
#                         dist + 1,
#                         (x + dx, y + dy),
#                         seen | {(x, y)},
#                     )
#                 )
#     assert best != 0
#     return best
# def part_two(data=data):
#     sx, sy = (data[0].index("."), int())
#     tx, ty = (data[-1].index("."), len(data.data) - 1)
#     todo = PrioQueue([(int(), int(), (tx, ty), frozenset())])
#     best = 0
#     for _heuristic, dist, (x, y), seen in todo:
#         if (x, y) in seen:
#             continue
#         if data[y][x] == "#" or y > ty:
#             continue
#         elif y == 0:
#             # best = max(best, dist)
#             return dist
#         else:
#             for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
#                 nx = x + dx
#                 ny = y + dy
#                 if ny > ty:
#                     continue
#                 todo.push(
#                     (
#                         -len(seen) - (abs(nx - sx) + abs(ny - sy)),
#                         dist + 1,
#                         (nx, ny),
#                         seen | {(x, y)},
#                     )
#                 )
#     assert best > 5638, best
#     return best
def part_two(data=data):
    sx, sy = (data[0].index("."), int())
    tx, ty = (data[-1].index("."), len(data.data) - 1)
    # first find nodes that are surrounded by 3 slopes
    nodes_of_interest = set[tuple[int, int]]()
    for x in range(len(data[0])):
        for y in range(len(data.data)):
            if data[y][x] == "#":
                continue
            if (
                data.orthogonal_neighbours(x, y)
                .filtered(lambda i: i[1] in ".<>^v")
                .len()
                != 2
            ):
                nodes_of_interest.add((x, y))
    print(len(nodes_of_interest))
    # for each node, find the paths to the nearby nodes
    paths = {}
    for node in nodes_of_interest:
        outputs = {}
        todo = []
        for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            x = node[0] + dx
            y = node[1] + dy
            if y < 0 or y > ty:
                continue
            if data[y][x] == "#":
                continue
            todo.append(((x, y), 1, (dx, dy)))
        while todo:
            pos, dist, last_dir = todo.pop()
            x, y = pos
            if y < 0 or y > ty:
                continue
            if pos in nodes_of_interest:
                outputs[pos] = dist
                continue
            for (nx, ny), val in data.orthogonal_neighbours(x, y):
                dx = x - nx
                dy = y - ny
                if (x - nx, y - ny) == last_dir:
                    continue
                if val == "#":
                    continue
                todo.append(((nx, ny), dist + 1, (-dx, -dy)))
        paths[node] = outputs
    todo = [
        (
            # (-sum(max(paths.values()) for paths in paths.values()), sx + sy),
            int(),
            (sx, sy),
            frozenset(),
        )
    ]

    best = 0
    done = {}
    printed = perf_counter()
    while todo:
        dist, pos, seen = todo.pop()
        # for (_heuristic, _), dist, pos, seen in todo:
        if pos in seen:
            continue
        if (pos, seen) in done and done[pos, seen] >= dist:
            continue
        done[pos, seen] = dist
        unseen_nodes = nodes_of_interest - seen
        best_possible = dist + sum(max(paths[pos].values()) for pos in unseen_nodes)
        if best_possible < best:
            continue

        if len(todo) % 5 == 0 and perf_counter() - printed > 1:
            print(len(todo), best, dist, pos)
            printed = perf_counter()
        if pos == (tx, ty):
            if dist > best:
                best = dist
                print("-- best --", best)
            continue
        next_seen = seen | {pos}
        for next_pos, next_dist in sorted(paths[pos].items(), key=lambda i: i[1]):
            todo.append(
                (
                    # (
                    #     -dist
                    #     - next_dist
                    #     - sum(
                    #         max(paths[pos].values())
                    #         for pos in unseen_nodes - {next_pos}
                    #     ),
                    #     abs(next_pos[0] - tx) + abs(next_pos[1] - ty),
                    # ),
                    dist + next_dist,
                    next_pos,
                    next_seen,
                )
            )
    # assert best > 5638, best
    return best


aoc_helper.lazy_test(day=23, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=23, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=23, year=2023, solution=part_two, data=data)
