from __future__ import annotations
from typing import Dict, List


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
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.x, self.y))

    def __iter__(self):
        return iter((self.x, self.y))

    def __sub__(self, other) -> Coord:
        assert isinstance(other, Coord)
        x = self.x - other.x
        y = self.y - other.y
        return Coord(x, y)


compass = [Coord(1, 0), Coord(0, 1), Coord(-1, 0), Coord(0, -1)]


def in_bounds(position: Coord, width: int, height: int):
    return (0 <= position.x < width) and (0 <= position.y < height)


def neighbours(start, elevation, width, height):
    start_elevation = elevation[start]
    for direction in compass:
        neighbour = start + direction
        if in_bounds(neighbour, width, height):
            if elevation[neighbour] - start_elevation == 1:
                yield neighbour


def walk_trail(trailhead, elevation, width, height):
    completed_trails = set()
    incomplete_trails = {(trailhead,)}
    while True:
        next_incomplete_trails = set()
        for trail in incomplete_trails:
            last_position = trail[-1]
            next_positions = neighbours(last_position, elevation, width, height)
            for neighbour in next_positions:
                if elevation[neighbour] == 9:
                    completed_trails.add((*trail, neighbour))
                else:
                    next_incomplete_trails.add((*trail, neighbour))
        incomplete_trails = next_incomplete_trails
        if len(incomplete_trails) == 0:
            return completed_trails


def print_trail(trail, elevation, width, height):
    sprites = {
        position: str(elevation[position])
        for position in trail}
    for y in range(height):
        row = list()
        for x in range(height):
            row.append(sprites.get(Coord(x, y), "."))
        print("".join(row))


def trailhead_ratings(topographic_map: List[str], verbose: bool = False) -> int:
    elevation: Dict[Coord, int] = dict()
    for y, line in enumerate(topographic_map):
        for x, char in enumerate(line):
            elevation[Coord(x, y)] = int(char)
    width = len(topographic_map[0])
    height = len(topographic_map)
    trailheads = {
        position: walk_trail(position, elevation, width, height)
        for position, altitude in elevation.items()
        if altitude == 0}
    # sort out how many unqique trails exist for each trailhead
    if verbose:
        for trailhead, trails in trailheads.items():
            explored = {position for trail in trails for position in trail}
            print_trail({trailhead, *explored}, elevation, width, height)
            print(f"rating={len(trails)}")
            print("=" * 10, end="\n\n")
    return sum(
        len(trails)
        for trailhead, trails in trailheads.items())


if __name__ == "__main__":
    test_topography = [
        "89010123",
        "78121874",
        "87430965",
        "96549874",
        "45678903",
        "32019012",
        "01329801",
        "10456732"]

    print("\nexample:")
    print(trailhead_ratings(test_topography, verbose=True))
    # expected output:
    # -- rating=20
    # -- rating=24
    # -- rating=10
    # -- rating=4
    # -- rating=1
    # -- rating=4
    # -- rating=5
    # -- rating=8
    # -- rating=5
    # -- 81

    with open("topographic_map.txt") as input_file:
        topography = [line.strip() for line in input_file]

    print("\nmain:")
    print(trailhead_ratings(topography))
