from typing import List, Tuple


Equation = Tuple[int, List[int]]


def calibrate(equations: List[Equation], verbose: bool = False) -> int:
    solutions = list()
    for equation in equations:
        target, components = equation
        if is_solvable(equation, verbose):
            solutions.append(target)
    return sum(solutions)


def iteration_passes(equation: Equation, run_number: int) -> bool:
    target, components = equation
    operation = [
        lambda a, b: a + b,
        lambda a, b: a * b,
        lambda a, b: int(f"{a}{b}")]  # concatenate
    result = components[0]
    for i, component in enumerate(components[1:]):
        op = (run_number // (3 ** i)) % 3
        result = operation[op](result, component)
        if result > target:
            return False
    return result == target


def iteration_string(components: List[str], run_number: int) -> str:
    out = [str(components[0])]
    for i, component in enumerate(components[1:]):
        op = (run_number // (3 ** i)) % 3
        out.extend(("+*|"[op], str(component)))
    return " ".join(out)


def is_solvable(equation: Equation, verbose: bool = False) -> bool:
    target, components = equation
    assert len(components) > 1
    # print(target)
    num_permutations = 3 ** len(components)
    for run_number in range(num_permutations):
        if iteration_passes(equation, run_number):
            if verbose:
                print(f"{target} = {iteration_string(components, run_number)}")
            return True
    return False


def parse(line: str) -> Equation:
    test_value, components = line.split(": ")
    return int(test_value), list(map(int, components.split()))


if __name__ == "__main__":
    test_input = [
        "190: 10 19",
        "3267: 81 40 27",
        "83: 17 5",
        "156: 15 6",
        "7290: 6 8 6 15",
        "161011: 16 10 13",
        "192: 17 8 14",
        "21037: 9 7 18 13",
        "292: 11 6 16 20"]
    test_equations = [
        parse(line)
        for line in test_input]

    print("\nexample:")
    print(calibrate(test_equations, verbose=True))
    # expected output:
    # -- 190 = 10 * 19
    # -- 3267 = 81 * 40 + 27  # or 81 + 40 * 27
    # -- 156 = 15 | 6
    # -- 7290 = 6 * 8 | 6 * 15
    # -- 192 = 17 | 8 + 14
    # -- 292 = 11 + 6 * 16 + 20
    # -- 11387

    with open("equations.txt") as input_file:
        equations = [
            parse(line)
            for line in input_file]

    print("\nmain:")
    print(calibrate(equations))
