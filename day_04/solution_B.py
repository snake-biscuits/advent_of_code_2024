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

    def __iter__(self):
        return iter((self.x, self.y))


base = (Coord(-1, -1), Coord(+1, -1), Coord(-1, +1), Coord(+1, +1))
rotations = [
    # M.S
    # .A.
    # M.S
    [base[i] for i in (0, 1, 2, 3)],
    # S.M
    # .A.
    # S.M
    [base[i] for i in (2, 3, 1, 0)],
    # M.M
    # .A.
    # S.S
    [base[i] for i in (0, 2, 1, 3)],
    # S.S
    # .A.
    # M.M
    [base[i] for i in (1, 3, 0, 2)]]


def find_xmas(word_search: List[str], verbose: bool = False) -> int:
    # spatial map
    cells = dict()
    for i, line in enumerate(word_search):
        for j, char in enumerate(line):
            if char in "XMAS":
                cells[(i, j)] = char
    # trace a line of letters from each A
    cells_with_xmas = dict()  # for verbose
    words_found = 0
    for a_pos in {pos for pos, char in cells.items() if char == "A"}:
        for positions in rotations:
            m1_pos = tuple((Coord(*a_pos) + positions[0]))
            m2_pos = tuple((Coord(*a_pos) + positions[1]))
            s1_pos = tuple((Coord(*a_pos) + positions[2]))
            s2_pos = tuple((Coord(*a_pos) + positions[3]))
            if all([
                cells.get(m1_pos, ".") == "M",
                cells.get(m2_pos, ".") == "M",
                cells.get(s1_pos, ".") == "S",
                cells.get(s2_pos, ".") == "S"]):
                words_found += 1
                cells_with_xmas.update({
                    pos: cells[pos] for pos in (
                        a_pos, m1_pos, m2_pos, s1_pos, s2_pos)})
    if verbose:
        for i, line in enumerate(word_search):
            print("".join([
                cells_with_xmas.get((i, j), ".")
                for j, char in enumerate(line)]))
    return words_found


if __name__ == "__main__":
    example = [
        "MMMSXXMASM",
        "MSAMXMSMSA",
        "AMXSXMAAMM",
        "MSAMASMSMX",
        "XMASAMXAMM",
        "XXAMMXXAMA",
        "SMSMSASXSS",
        "SAXAMASAAA",
        "MAMMMXMMMM",
        "MXMXAXMASX"]

    print("\nexample:")
    print(find_xmas(example, verbose=True))
    # expected output:
    # -- .M.S......
    # -- ..A..MSMS.
    # -- .M.S.MAA..
    # -- ..A.ASMSM.
    # -- .M.S.M....
    # -- ..........
    # -- S.S.S.S.S.
    # -- .A.A.A.A..
    # -- M.M.M.M.M.
    # -- ..........
    # -- 9

    with open("wordsearch.txt") as input_file:
        lines = input_file.readlines()

    print("\nmain:")
    print(find_xmas(lines))
