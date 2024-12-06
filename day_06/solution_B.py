from __future__ import annotations
import collections
import copy
from typing import List


class Coord:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Coord({self.x}, {self.y})"

    def __add__(self, other) -> Coord:
        assert isinstance(other, Coord)
        x = self.x + other.x
        y = self.y + other.y
        return Coord(x, y)

    def __eq__(self, other) -> bool:
        assert isinstance(other, Coord)
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __iter__(self):
        return iter((self.x, self.y))


compass = [
    Coord(0, -1),  # (^) North
    Coord(1, 0),   # (>) East
    Coord(0, 1),   # (v) South
    Coord(-1, 0)]  # (<) West


guard_sprite = {
    compass[i]: char
    for i, char in enumerate("^>v<")}


def in_area(guard: Coord, width: int, height: int):
    return all([
        0 <= guard.x < width,
        0 <= guard.y < height])


def print_route(guard_start, floor_dimensions, obstructions, route_dirs, trap):
    # gather sprites
    sprites = {
        **{pos: "#" for pos in obstructions},
        **{trap: "O"}}
    # draw the route over the top of everything (except the guard)
    route_sprites = dict()
    for tile, dirs in route_dirs.items():
        north_south = (compass[0] in dirs or compass[2] in dirs)
        east_west = (compass[1] in dirs or compass[3] in dirs)
        route_sprites[tile] = {
            (north_south and not east_west): "|",
            (east_west and not north_south): "-",
            (east_west and north_south): "+"}[True]
        if tile in sprites:
            route_sprites[tile] = "X"  # bad
    sprites.update(route_sprites)
    # draw the guard on the top of the route
    guard_pos, guard_dir = guard_start
    sprites.update({guard_pos: guard_sprite[guard_dir]})
    # put sprites over the base map
    floor_height, floor_width = floor_dimensions
    for y in range(floor_height):
        row = list()
        for x in range(floor_width):
            tile = Coord(x, y)
            row.append(sprites.get(tile, "."))
        print("".join(row))


def simulate_guard(guard_pos, guard_dir, obstructions):
    next_position = guard_pos + guard_dir
    if next_position in obstructions:
        # turn right 90 degrees
        dir_index = compass.index(guard_dir)
        guard_dir = compass[(dir_index + 1) % 4]
    else:
        # take 1 step forwards
        guard_pos = next_position
    return guard_pos, guard_dir


# NOTE: this is really slow
def trap_route(guard, floor, route_dirs, obstructions):
    guard_pos, guard_dir = guard
    alt_route_dirs = copy.deepcopy(route_dirs)  # don't pollute route
    while in_area(guard_pos, *floor):
        # check for looping
        next_pos = guard_pos + guard_dir
        if next_pos in alt_route_dirs:
            if guard_dir in alt_route_dirs[next_pos]:
                # print(f"loop detected: {guard_sprite[guard_dir]} @ {guard_pos}")
                # TODO: trap positions are correct, but don't print in full
                return alt_route_dirs  # guard is looping
        # simulate 1 tick
        alt_route_dirs[guard_pos].add(guard_dir)
        guard_pos, guard_dir = simulate_guard(guard_pos, guard_dir, obstructions)
    return None  # didn't loop


def trap_positions(floor_plan: List[str], verbose: bool = False) -> int:
    # parse floor_plan
    floor_height = len(floor_plan)
    floor_width = len(floor_plan[0])
    floor = (floor_width, floor_height)
    # get points of interest
    obstructions = set()
    for y, row in enumerate(floor_plan):
        for x, char in enumerate(row):
            if char == "#":
                obstructions.add(Coord(x, y))
            elif char == "^":
                guard_pos = Coord(x, y)
                guard_dir = compass[0]  # (^) North
                guard_start = (guard_pos, guard_dir)
    # simulate patrol
    route_dirs = collections.defaultdict(set)
    traps = set()
    # ^ [(position, direction)]
    while in_area(guard_pos, *floor):
        # test if a trap in front of the guard will create a loop
        next_pos = guard_pos + guard_dir
        can_be_trapped = all([
            next_pos not in route_dirs,
            next_pos not in obstructions])
        if can_be_trapped:
            guard = (guard_pos, guard_dir)
            all_obstructions = {*obstructions, next_pos}
            alt_route = trap_route(guard, floor, route_dirs, all_obstructions)
            if alt_route is not None:
                traps.add(next_pos)
                if verbose:
                    print_route(guard_start, floor, obstructions, alt_route, next_pos)
                    print()
        # simulation as usual
        route_dirs[guard_pos].add(guard_dir)
        guard_pos, guard_dir = simulate_guard(guard_pos, guard_dir, obstructions)
    return len(traps)


if __name__ == "__main__":
    test_input = [
        "....#.....",
        ".........#",
        "..........",
        "..#.......",
        ".......#..",
        "..........",
        ".#..^.....",
        "........#.",
        "#.........",
        "......#..."]

    print("\nexample:")
    print(trap_positions(test_input, verbose=True))
    # expected output:
    # -- ....#.....
    # -- ....+---+#
    # -- ....|...|.
    # -- ..#.|...|.
    # -- ....|..#|.
    # -- ....|...|.
    # -- .#.O^---+.
    # -- ........#.
    # -- #.........
    # -- ......#...
    # --
    # -- ....#.....
    # -- ....+---+#
    # -- ....|...|.
    # -- ..#.|...|.
    # -- ..+-+-+#|.
    # -- ..|.|.|.|.
    # -- .#+-^-+-+.
    # -- ......O.#.
    # -- #.........
    # -- ......#...
    # --
    # -- ....#.....
    # -- ....+---+#
    # -- ....|...|.
    # -- ..#.|...|.
    # -- ..+-+-+#|.
    # -- ..|.|.|.|.
    # -- .#+-^-+-+.
    # -- .+----+O#.
    # -- #+----+...
    # -- ......#...
    # --
    # -- ....#.....
    # -- ....+---+#
    # -- ....|...|.
    # -- ..#.|...|.
    # -- ..+-+-+#|.
    # -- ..|.|.|.|.
    # -- .#+-^-+-+.
    # -- ..|...|.#.
    # -- #O+---+...
    # -- ......#...
    # --
    # -- ....#.....
    # -- ....+---+#
    # -- ....|...|.
    # -- ..#.|...|.
    # -- ..+-+-+#|.
    # -- ..|.|.|.|.
    # -- .#+-^-+-+.
    # -- ....|.|.#.
    # -- #..O+-+...
    # -- ......#...
    # --
    # -- ....#.....
    # -- ....+---+#
    # -- ....|...|.
    # -- ..#.|...|.
    # -- ..+-+-+#|.
    # -- ..|.|.|.|.
    # -- .#+-^-+-+.
    # -- .+----++#.
    # -- #+----++..
    # -- ......#O..
    # --
    # -- 6

    with open("map.txt") as input_file:
        floor_plan = [line.strip() for line in input_file]

    print("\nmain:")
    print(trap_positions(floor_plan))
