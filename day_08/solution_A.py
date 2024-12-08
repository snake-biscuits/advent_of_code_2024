from __future__ import annotations
import collections
import itertools
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


def antinode_locations(city_map: List[str], verbose: bool = False) -> int:
    # map the city
    antennae = collections.defaultdict(set)
    for y, line in enumerate(city_map):
        for x, char in enumerate(line):
            if char != ".":
                antennae[char].add(Coord(x, y))

    # generate antinodes
    antinodes = collections.defaultdict(set)
    for frequency in antennae:
        for A, B in itertools.combinations(antennae[frequency], 2):
            diff = A - B
            antinodes[frequency].update({A + diff, B - diff})

    width = len(city_map[0])
    height = len(city_map)
    # if verbose:
    #     for frequency in antinodes:
    #         print(f"{frequency} antinodes")
    #         print_map(width, height, antennae, antinodes[frequency])
    #         print()

    # bounds testing
    antinodes = {
        position
        for frequency, positions in antinodes.items()
        for position in positions
        if (0 <= position.x < width)
        and (0 <= position.y < height)}
    # result
    if verbose:
        print_map(width, height, antennae, antinodes)
    return len(antinodes)


def print_map(width, height, antennae, antinodes):
    sprites = {
        **{
            position: "#"
            for position in antinodes},
        **{
            position: frequency
            for frequency, positions in antennae.items()
            for position in positions}}
    for y in range(height):
        row = list()
        for x in range(width):
            row.append(sprites.get(Coord(x, y), "."))
        print("".join(row))


if __name__ == "__main__":
    test_map = [
        "............",
        "........0...",
        ".....0......",
        ".......0....",
        "....0.......",
        "......A.....",
        "............",
        "............",
        "........A...",
        ".........A..",
        "............",
        "............"]

    print("\nexample:")
    print(antinode_locations(test_map, verbose=True))
    # expected output:
    # -- ......#....#
    # -- ...#....0...
    # -- ....#0....#.
    # -- ..#....0....
    # -- ....0....#..
    # -- .#....A.....
    # -- ...#........
    # -- #......#....
    # -- ........A...
    # -- .........A..
    # -- ..........#.
    # -- ..........#.
    # -- 14

    with open("antennae.txt") as input_file:
        city_map = [line.strip() for line in input_file]

    print("\nmain:")
    print(antinode_locations(city_map))
