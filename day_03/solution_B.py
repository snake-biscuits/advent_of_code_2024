import re


def parse(memory: str, verbose: bool = False) -> int:
    pattern = re.compile(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)|do\(\)|don't\(\)")
    do = True
    muls = list()
    for match in pattern.finditer(memory):
        substring = match.string[match.start():match.end()]
        if substring == "do()":
            do = True
        elif substring == "don't()":
            do = False
        elif substring.startswith("mul"):
            if do:
                muls.append(match.groups())
    if verbose:
        for a, b in muls:
            print(f"mul({a},{b})")
    return sum([
        int(a) * int(b)
        for a, b in muls])


if __name__ == "__main__":
    test_input = """
    xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
    """

    print("\nexample:")
    print(parse(test_input, verbose=True))
    # expected output:
    # -- mul(2,4)
    # -- mul(8,5)
    # -- 48

    with open("memory.txt") as input_file:
        memory = input_file.read()

    print("\nmain:")
    print(parse(memory))
