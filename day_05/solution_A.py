from typing import List


def middle_pages(instructions: List[str], verbose: bool = False) -> int:
    order_rules = list()
    updates = list()
    for line in instructions:
        if "|" in line:  # ordering rule
            first, second = map(int, line.split("|"))
            order_rules.append((first, second))
        elif "," in line:  # update order
            updates.append(tuple(map(int, line.split(","))))
    middles = list()
    for update in updates:
        if all([
            update.index(first) < update.index(second)
            for first, second in order_rules
            if first in update and second in update]):
            middle_index = len(update) // 2
            middles.append(update[middle_index])
            if verbose:
                # TODO: relevant rules
                print(",".join(map(str, update)))
    return sum(middles)


if __name__ == "__main__":
    sample = [
        "47|53",
        "97|13",
        "97|61",
        "97|47",
        "75|29",
        "61|13",
        "75|53",
        "29|13",
        "97|29",
        "53|29",
        "61|53",
        "97|53",
        "61|29",
        "47|13",
        "75|47",
        "97|75",
        "47|61",
        "75|61",
        "47|29",
        "75|13",
        "53|13",
        "75,47,61,53,29",
        "97,61,53,29,13",
        "75,29,13",
        "75,97,47,61,53",
        "61,13,29",
        "97,13,75,29,47"]

    print("\nexample:")
    print(middle_pages(sample, verbose=True))
    # expected output:
    # -- 75,47,61,53,29
    # -- 97,61,53,29,13
    # -- 75,29,13
    # -- 143

    with open("rules_and_updates.txt") as input_file:
        instructions = input_file.readlines()

    print("\nmain:")
    print(middle_pages(instructions))
