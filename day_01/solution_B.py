from typing import List, Tuple


def similarity_score(vertical_lists: List[Tuple[int, int]], verbose: bool = False) -> int:
    left, right = list(zip(*vertical_lists))

    counts = {
        a: right.count(a)
        for a in set(left)}

    scores = [
        a * counts[a]
        for a in left]

    if verbose:
        print(" + ".join(map(str, scores)))

    return sum(scores)


if __name__ == "__main__":
    test_input = [
        (3, 4),
        (4, 3),
        (2, 5),
        (1, 3),
        (3, 9),
        (3, 3)]

    print("\nexample:")
    print(similarity_score(test_input, verbose=True))
    # expected ouput:
    # -- 9 + 4 + 0 + 0 + 9 + 9
    # -- 31

    with open("historic_locations.txt") as input_file:
        two_lists = [
            tuple(map(int, line.split("  ")))
            for line in input_file]

    print("\nmain:")
    print(similarity_score(two_lists))
