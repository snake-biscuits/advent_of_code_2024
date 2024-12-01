from typing import List, Tuple


def similarity_score(vertical_lists: List[Tuple[int, int]]) -> int:
    left, right = list(zip(*vertical_lists))

    counts = {
        a: right.count(a)
        for a in set(left)}

    return sum(
        a * counts[a]
        for a in left)


if __name__ == "__main__":
    # test_input = [
    #     (3, 4),
    #     (4, 3),
    #     (2, 5),
    #     (1, 3),
    #     (3, 9),
    #     (3, 3)]

    # print(similarity_score(test_input))  # 11

    two_lists = list()
    with open("historic_locations.txt") as input_file:
        two_lists = [
            tuple(map(int, line.split("  ")))
            for line in input_file]

    print(similarity_score(two_lists))
