from typing import List


def blink(stones: List[int]) -> List[int]:
    out = list()
    for stone in stones:
        stone_text = str(stone)
        if stone == 0:
            out.append(1)
        elif len(stone_text) % 2 == 0:
            half_index = len(stone_text) // 2
            out.append(int(stone_text[:half_index]))
            out.append(int(stone_text[half_index:]))
        else:
            out.append(stone * 2024)
    return out


def count_stones(stone_text: str, verbose: bool = False) -> int:
    stones = map(int, stone_text.split(" "))
    for i in range(25):
        stones = blink(stones)
        if verbose and i < 7:
            print(f"After {i + 1} blinks:")
            print(*stones)
            print()
    return len(stones)


if __name__ == "__main__":
    test_stones = "125 17"

    print("\nexample:")
    print(count_stones(test_stones, verbose=True))
    # expected output:
    # -- verbose line
    # -- 55312

    with open("stones.txt") as input_file:
        stones = input_file.read().strip()

    print("\nmain:")
    print(count_stones(stones))
