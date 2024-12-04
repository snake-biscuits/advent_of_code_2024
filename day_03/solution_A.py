import re


def parse(memory: str, verbose: bool = False) -> int:
    pattern = re.compile(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)")
    muls = pattern.findall(memory)
    if verbose:
        print(f"mul({a},{b})" for a, b in muls)
    return sum([
        int(a) * int(b)
        for a, b in muls])


if __name__ == "__main__":
    test_input = """
    xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
    """

    print("\nexample:")
    print(parse(test_input, verbose=True))
    # expected output:
    # -- mul(2,4)
    # -- mul(5,5)
    # -- mul(11,8)
    # -- mul(8,5)
    # -- 161

    with open("memory.txt") as input_file:
        memory = input_file.read()

    print("\nmain:")
    print(parse(memory))
