from typing import List


def starship(a: int, b: int):
    return {
        a < b: +1,  # increase
        a == b: 0,
        a > b: -1,  # decrease
        }[True]


def is_safe(report: List[int], verbose=False) -> bool:
    a, b = report[:2]
    if not 1 <= abs(a - b) <= 3:
        return False
    direction = starship(a, b)
    for a, b in zip(report[1:], report[2:]):
        if starship(a, b) != direction or not 1 <= abs(a - b) <= 3:
            return False
    else:
        if verbose:
            print(f"SAFE: {report}")
        return True

def num_safe(reports: List[List[int]], verbose=False):
    unsafe_reports = [
        report
        for report in reports
        if not is_safe(report, verbose)]
    truly_unsafe_reports = list()
    for report in unsafe_reports:
        for i, x in enumerate(report):
            modified_report = [
                *report[:i],
                *report[i+1:]]
            if is_safe(modified_report, verbose):
                if verbose:
                    print(f"^ removed level {i+1} ({x})")
                break
        else:
            truly_unsafe_reports.append(report)
    return len(reports) - len(truly_unsafe_reports)

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
    # -- SAFE: (1, 2, 4, 5)
    # -- ^ removed level 2 (3)
    # -- SAFE: (8, 6, 4, 1)
    # -- ^ removed level 3 (4)
    # -- SAFE: (1, 3, 6, 7, 9)
    # -- 4

    with open("reports.txt") as input_file:
        reports = [
            tuple(map(int, line.split(" ")))
            for line in input_file]

    print("\nmain:")
    print(num_safe(reports))

