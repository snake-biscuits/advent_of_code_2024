from __future__ import annotations
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


def in_area(guard: Coord, width: int, height: int):
    return all([
        0 <= guard.x < width,
        0 <= guard.y < height])


def guard_route(floor_plan: List[str], verbose: bool = False) -> int:
    floor_height = len(floor_plan)
    floor_width = len(floor_plan[0])
    # get points of interest
    obstructions = set()
    for y, row in enumerate(floor_plan):
        for x, char in enumerate(row):
            if char == "#":
                obstructions.add(Coord(x, y))
            elif char == "^":
                guard_pos = Coord(x, y)
                guard_dir = compass[0]  # (^) North
    # simulate patrol
    route = {guard_pos}
    while in_area(guard_pos, floor_width, floor_height):
        route.add(guard_pos)
        next_position = guard_pos + guard_dir
        if next_position in obstructions:
            # turn 90 degrees right
            dir_index = compass.index(guard_dir)
            guard_dir = compass[(dir_index + 1) % 4]
        else:
            # take 1 step forwards
            guard_pos = next_position
    if verbose:
        for y in range(floor_height):
            row = list()
            for x in range(floor_width):
                tile = Coord(x, y)
                if tile in obstructions:
                    row.append("#")
                elif tile in route:
                    row.append("X")
                else:
                    row.append(".")
            print("".join(row))
    return len(route)

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
    print(guard_route(test_input, verbose=True))
    # expected output:
    # -- ....#.....
    # -- ....XXXXX#
    # -- ....X...X.
    # -- ..#.X...X.
    # -- ..XXXXX#X.
    # -- ..X.X.X.X.
    # -- .#XXXXXXX.
    # -- .XXXXXXX#.
    # -- #XXXXXXX..
    # -- ......#X..
    # -- 41

    with open("map.txt") as input_file:
        floor_plan = [line.strip() for line in input_file]

    print("\nmain:")
    print(guard_route(floor_plan))
