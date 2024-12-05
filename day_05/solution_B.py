from typing import List


def middle_pages(instructions: List[str], verbose: bool = False) -> int:
    # order_rules = {first: {second}}
    order_rules = set()
    updates = list()
    for line in instructions:
        if "|" in line:  # ordering rule
            first, second = map(int, line.split("|"))
            order_rules.add((first, second))
        elif "," in line:  # update order
            updates.append(tuple(map(int, line.split(","))))
    middles = list()
    for update in updates:
        rules = {
            (first, second)
            for first, second in order_rules
            if first in update and second in update}
        if not all([
            update.index(first) < update.index(second)
            for first, second in rules]):
            iterations = 0
            sorted_update = list(update)
            while not all([
                sorted_update.index(first) < sorted_update.index(second)
                for first, second in rules]):
                iterations += 1
                if iterations > 50:
                    print("!!!")
                    print(f"{rules=}")
                    print(f"{update=}")
                    print(f"{sorted_update=}")
                    raise RuntimeError("taking too long to sort")
                # swap sort
                for page in sorted_update:
                    for first, second in rules:
                        if not page == second:
                            continue
                        first_index = sorted_update.index(first)
                        second_index = sorted_update.index(second)
                        if first_index > second_index:
                            sorted_update[first_index] = second
                            sorted_update[second_index] = first
            # DEBUG
            if verbose:
                print(*[f"{f}|{s}" for f, s in rules], sep="\n")
                print(
                    ",".join(map(str, update)),
                    "->",
                    ",".join(map(str, sorted_update)))
                print("")
            assert all([
                sorted_update.index(first) < sorted_update.index(second)
                for first, second in rules]), "failed to follow a rule"
            middle_index = len(sorted_update) // 2
            middles.append(sorted_update[middle_index])
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
    # -- 75,97,47,61,53 -> 97,75,47,61,53
    # -- 61,13,29 -> 61,29,13
    # -- 97,13,75,29,47 -> 97,75,47,29,13
    # -- 123

    with open("rules_and_updates.txt") as input_file:
        instructions = input_file.readlines()

    print("\nmain:")
    print(middle_pages(instructions))
