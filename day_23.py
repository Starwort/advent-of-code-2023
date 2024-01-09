import aoc_helper
from aoc_helper import Grid, PrioQueue, list

raw = aoc_helper.fetch(23, 2023)


def parse_raw(raw: str) -> tuple[list[tuple[int, int, bool]], list[int]]:
    data = Grid.from_string(raw, str)

    sx, sy = (data[0].index("."), int())
    tx, ty = (data[-1].index("."), len(data.data) - 1)
    # first find nodes that are surrounded by 3 slopes
    nodes_of_interest = list[tuple[int, int]]()
    for y, row in data.data.enumerated():
        for x, cell in row.enumerated():
            if cell != ".":
                continue
            if (
                data.orthogonal_neighbours(x, y)
                .filtered(lambda i: i[1] in ".<>^v")
                .len()
                != 2
            ):
                nodes_of_interest.append((x, y))
    # for each node, find the paths to the nearby nodes
    paths = list()
    for i, node in nodes_of_interest.enumerated():
        if i == 0:
            assert node == (sx, sy), f"{i=} {node=} {(sx, sy)=}"
        elif i == len(nodes_of_interest) - 1:
            assert node == (tx, ty), f"{i=} {node=} {(tx, ty)=}"
        outputs = []
        todo = []
        for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            x = node[0] + dx
            y = node[1] + dy
            if y < 0 or y > ty or data[y][x] == "#":
                continue
            todo.append(((x, y), 1, (dx, dy)))
        while todo:
            node, dist, (dx, dy) = todo.pop()
            x, y = node
            if y < 0 or y > ty:
                continue
            if node in nodes_of_interest:
                outputs.append(
                    (
                        nodes_of_interest.index(node),
                        dist,
                        {
                            ".": False,
                            "^": dy != -1,
                            "v": dy != 1,
                            "<": dx != -1,
                            ">": dx != 1,
                        }[data[y][x]],
                    )
                )
                continue
            for dx, dy in ((dx, dy), (dy, -dx), (-dy, dx)):
                nx = x + dx
                ny = y + dy
                if data[ny][nx] != "#":
                    todo.append(((nx, ny), dist + 1, (dx, dy)))
        outputs.sort(key=lambda i: i[1])
        paths.append(outputs)
    path_maxes = list(max(i[1] for i in paths) for paths in paths)

    return paths, path_maxes


data = parse_raw(raw)


# providing this default is somewhat of a hack - there isn't any other way to
# force type inference to happen, AFAIK - but this won't work with standard
# collections (list, set, dict, tuple)
def part_one(data=data):
    paths, path_maxes = data
    todo = PrioQueue(
        [
            (
                -sum(path_maxes),
                int(),
                int(),
                int(),
            )
        ]
    )

    best = 0
    target = len(paths) - 1
    for best_possible, dist, node, visited in todo:
        this_visit = 1 << node
        if visited & this_visit or best_possible < best:
            continue
        visited |= this_visit

        if node == target:
            if dist > best:
                best = dist
                print("-- best --", best)
            continue

        best_possible += path_maxes[node]

        for next_pos, next_dist, p2_only in paths[node]:
            if p2_only:
                continue
            todo.push(
                (
                    best_possible - next_dist,
                    dist + next_dist,
                    next_pos,
                    visited,
                )
            )
    return best


aoc_helper.lazy_test(day=23, year=2023, parse=parse_raw, solution=part_one)


def part_two(data=data):
    paths, path_maxes = data
    todo = PrioQueue(
        [
            (
                -sum(path_maxes),
                int(),
                int(),
                int(),
            )
        ]
    )

    best = 0
    target = len(paths) - 1
    for best_possible, dist, node, visited in todo:
        this_visit = 1 << node
        if visited & this_visit or best_possible < best:
            continue
        visited |= this_visit

        if node == target:
            if dist > best:
                best = dist
                print("-- best --", best)
            continue

        best_possible += path_maxes[node]

        for next_pos, next_dist, _p2_only in paths[node]:
            todo.push(
                (
                    best_possible - next_dist,
                    dist + next_dist,
                    next_pos,
                    visited,
                )
            )
    return best


aoc_helper.lazy_test(day=23, year=2023, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=23, year=2023, solution=part_one, data=data)
aoc_helper.lazy_submit(day=23, year=2023, solution=part_two, data=data)
