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

compass = [
    Coord(-1, -1), Coord(-1, 0), Coord(-1, 1),
    Coord(0, -1), Coord(0, 1),
    Coord(1, -1), Coord(1, 0), Coord(1, 1)]



def find_xmas(word_search: List[str], verbose: bool = False) -> int:
    # spatial map
    cells = dict()
    for i, line in enumerate(word_search):
        for j, char in enumerate(line):
            if char in "XMAS":
                cells[(i, j)] = char
    # trace a line of letters from each X
    cells_with_xmas = dict()  # for verbose
    words_found = 0
    for x_pos in {pos for pos, char in cells.items() if char == "X"}:
        for direction in compass:
            m_pos = tuple((Coord(*x_pos) + direction))
            a_pos = tuple((Coord(*m_pos) + direction))
            s_pos = tuple((Coord(*a_pos) + direction))
            if all([
                cells.get(m_pos, ".") == "M",
                cells.get(a_pos, ".") == "A",
                cells.get(s_pos, ".") == "S"]):
                words_found += 1
                cells_with_xmas.update({
                    x_pos: "X", m_pos: "M", a_pos: "A", s_pos: "S"})
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
    # -- ....XXMAS.
    # -- .SAMXMS...
    # -- ...S..A...
    # -- ..A.A.MS.X
    # -- XMASAMX.MM
    # -- X.....XA.A
    # -- S.S.S.S.SS
    # -- .A.A.A.A.A
    # -- ..M.M.M.MM
    # -- .X.X.XMASX
    # -- 18

    with open("wordsearch.txt") as input_file:
        lines = input_file.readlines()

    print("\nmain:")
    print(find_xmas(lines))
