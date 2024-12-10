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


def neighbours(start, elevations, width, height):
    start_elevation = elevations[start]
    for direction in compass:
        neighbour = start + direction
        if in_bounds(neighbour, width, height):
            if elevations[neighbour] - start_elevation == 1:
                yield neighbour


def walk_trail(start, elevations, width, height):
    out = set()
    for neighbour in neighbours(start, elevations, width, height):
        out = {
            *out,
            neighbour,
            *walk_trail(neighbour, elevations, width, height)}
    return out


def print_trail(trail, elevations, width, height):
    sprites = {
        position: str(elevations[position])
        for position in trail}
    for y in range(height):
        row = list()
        for x in range(height):
            row.append(sprites.get(Coord(x, y), "."))
        print("".join(row))


def trailhead_scores(topographic_map: List[str], verbose: bool = False) -> int:
    elevations: Dict[Coord, int] = dict()
    for y, line in enumerate(topographic_map):
        for x, char in enumerate(line):
            elevations[Coord(x, y)] = int(char)
    width = len(topographic_map[0])
    height = len(topographic_map)
    trailheads = {
        position: walk_trail(position, elevations, width, height)
        for position, elevation in elevations.items()
        if elevation == 0}
    if verbose:
        for trailhead, trail in trailheads.items():
            # print_trail({trailhead, *trail}, elevations, width, height)
            print(len([position for position in trail if elevations[position] == 9]))
            # print()
    return sum(
        len([position for position in trail if elevations[position] == 9])
        for trailhead, trail in trailheads.items())


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
    print(trailhead_scores(test_topography, verbose=True))
    # expected output:
    # -- 36

    with open("topographic_map.txt") as input_file:
        topography = [line.strip() for line in input_file]

    print("\nmain:")
    print(trailhead_scores(topography))
