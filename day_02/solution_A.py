from typing import List


def starship(a: int, b: int):
    return {
        a < b: +1,  # increase
        a == b: 0,
        a > b: -1,  # decrease
        }[True]


def num_safe(reports: List[List[int]], verbose=False) -> int:
    out = 0
    for report in reports:
        # NOTE: a do, while would be perfect for this
        a, b = report[:2]
        direction = starship(a, b)
        if not 1 <= abs(a - b) <= 3:
            if verbose:
                print(f"FAIL: {report} {a} {b}")
            continue  # first compare fails
        for a, b in zip(report[1:], report[2:]):
            if starship(a, b) != direction or not 1 <= abs(a - b) <= 3:
                if verbose:
                    print(f"FAIL: {report} {a} {b}")
                break
        else:
            if verbose:
                print("PASS:", report)
            out += 1
    return out

if __name__ == "__main__":
    small_reports = [
        (7, 6, 4, 2, 1),
        (1, 2, 7, 8, 9),
        (9, 7, 6, 2, 1),
        (1, 3, 2, 4, 5),
        (8, 6, 4, 4, 1),
        (1, 3, 6, 7, 9)]

    print("\nexample:")
    print(num_safe(small_reports, verbose=True))
    # expected output:
    # -- SAFE: (7, 6, 4, 2, 1)
    # -- SAFE: (1, 3, 6, 7, 9)
    # -- 2

    with open("reports.txt") as input_file:
        reports = [
            tuple(map(int, line.split(" ")))
            for line in input_file]

    print("\nmain:")
    print(num_safe(reports))
