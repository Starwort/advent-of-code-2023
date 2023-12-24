#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum GridInfo {
    Empty,
    Wall,
    SlopeUp,
    SlopeDown,
    SlopeLeft,
    SlopeRight,
}

fn main() {
    let mut grid = [[GridInfo::Empty; 141]; 141];
    let input = raoc::sync_fetch(23, 2023, false);
    for (y, line) in input.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            grid[y][x] = match c {
                '.' => GridInfo::Empty,
                '#' => GridInfo::Wall,
                '^' => GridInfo::SlopeUp,
                'v' => GridInfo::SlopeDown,
                '<' => GridInfo::SlopeLeft,
                '>' => GridInfo::SlopeRight,
                _ => panic!("Bad input: found '{c}'"),
            };
        }
    }
    let grid = grid;

    let orthogonal_spaces = |x: usize, y: usize| {
        let mut count = 0;
        if x > 0 && grid[y][x - 1] != GridInfo::Wall {
            count += 1;
        }
        if x < 140 && grid[y][x + 1] != GridInfo::Wall {
            count += 1;
        }
        if y > 0 && grid[y - 1][x] != GridInfo::Wall {
            count += 1;
        }
        if y < 140 && grid[y + 1][x] != GridInfo::Wall {
            count += 1;
        }
        count
    };

    let mut nodes_of_interest = Vec::new();
    for (y, row) in grid.iter().enumerate() {
        for (x, &cell) in row.iter().enumerate() {
            if cell == GridInfo::Empty && orthogonal_spaces(x, y) != 2 {
                nodes_of_interest.push((x, y));
            }
        }
    }

    let mut paths = Vec::new();
    for (i, &(x, y)) in nodes_of_interest.iter().enumerate() {
        if i == 0 {
            assert_eq!(y, 0);
        } else if i == nodes_of_interest.len() - 1 {
            assert_eq!(y, 140);
        }
        let mut outputs = Vec::new();
        let mut todo = Vec::new();
        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)] {
            let nx = x.wrapping_add_signed(dx);
            let ny = y.wrapping_add_signed(dy);
            if nx > 140 || ny > 140 {
                continue;
            }
            todo.push((
                nx,
                ny,
                1,
                dx,
                dy,
                match grid[ny][nx] {
                    GridInfo::Empty => false,
                    GridInfo::SlopeUp => dy != -1,
                    GridInfo::SlopeDown => dy != 1,
                    GridInfo::SlopeLeft => dx != -1,
                    GridInfo::SlopeRight => dx != 1,
                    GridInfo::Wall => continue,
                },
            ));
        }
        while let Some((x, y, dist, dx, dy, p2_only)) = todo.pop() {
            if let Some(i) = nodes_of_interest.iter().position(|&val| val == (x, y)) {
                outputs.push((i, dist, p2_only));
                continue;
            }
            for (dx, dy) in [(dx, dy), (dy, -dx), (-dy, dx)] {
                let nx = x.wrapping_add_signed(dx);
                let ny = y.wrapping_add_signed(dy);
                if grid[ny][nx] != GridInfo::Wall {
                    todo.push((nx, ny, dist + 1, dx, dy, p2_only));
                }
            }
        }
        outputs.sort_unstable_by_key(|&(_, dist, _)| dist);
        paths.push(outputs);
    }
    let paths = paths;
    println!("{}", solve(&paths, false));
    println!("{}", solve(&paths, true));
}

fn solve(paths: &[Vec<(usize, usize, bool)>], p2: bool) -> usize {
    let path_maxes = paths
        .iter()
        .map(|paths| {
            paths
                .iter()
                .filter_map(
                    |&(_, dist, p2_only)| {
                        if p2 || !p2_only {
                            Some(dist)
                        } else {
                            None
                        }
                    },
                )
                .max()
                .unwrap()
        })
        .collect::<Vec<_>>();
    let mut todo = vec![(
        0usize, // distance
        0usize, // current node
        0u64,   // visited
        path_maxes.iter().copied().sum::<usize>(),
    )];
    let mut best = 0;

    while let Some((dist, node, visited, best_possible)) = todo.pop() {
        let this_visit = 1 << node;
        if visited & this_visit != 0 || best_possible <= best {
            continue;
        }
        let visited = visited | this_visit;

        if node == paths.len() - 1 {
            best = best.max(dist);
            continue;
        }

        let best_possible = best_possible - path_maxes[node];

        for (next_node, next_dist, p2_only) in &paths[node] {
            if (p2 || !p2_only) && visited & (1 << next_node) == 0 {
                todo.push((
                    dist + next_dist,
                    *next_node,
                    visited,
                    best_possible + next_dist,
                ));
            }
        }
    }

    best
}
