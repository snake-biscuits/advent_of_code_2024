from typing import List, Tuple


def total_difference(vertical_lists: List[Tuple[int, int]], verbose: bool = False) -> int:
    left, right = list(zip(*vertical_lists))

    differences = [
        abs(a - b)
        for a, b in zip(sorted(left), sorted(right))]

    if verbose:
        print(" + ".join(map(str, differences)))

    return sum(differences)


if __name__ == "__main__":
    test_input = [
        (3, 4),
        (4, 3),
        (2, 5),
        (1, 3),
        (3, 9),
        (3, 3)]

    print("\nexample:")
    print(total_difference(test_input, verbose=True))
    # expected output:
    # -- 2 + 1 + 0 + 1 + 2 + 5
    # -- 11

    two_lists = list()
    with open("historic_locations.txt") as input_file:
        two_lists = [
            tuple(map(int, line.split("  ")))
            for line in input_file]

    print("\nmain:")
    print(total_difference(two_lists))
