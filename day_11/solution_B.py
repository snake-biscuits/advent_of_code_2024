from typing import List
import functools


# NOTE: we can leverage recursive patterns
# -- 0 -> 1 -> 2024 -> 20 24 -> 2 0 2 4 (then 0 -> 1)


@functools.cache  # <- obscenely OP
def blink(stone: int, count: int) -> int:
    if count == 0:
        return 1  # stolen from timoreo's solution, my cpu was frying
    stone_text = str(stone)
    if stone == 0:
        return blink(1, count - 1)
    elif len(stone_text) % 2 == 0:
        half_index = len(stone_text) // 2
        left = int(stone_text[:half_index])
        right = int(stone_text[half_index:])
        return blink(left, count - 1) + blink(right, count - 1)
    else:
        return blink(stone * 2024, count - 1)



def count_stones(stone_text: str, verbose: bool = False) -> int:
    stones = list(map(int, stone_text.split(" ")))
    count = 0
    for stone in stones:
        count += blink(stone, 75)
    return count


if __name__ == "__main__":
    with open("stones.txt") as input_file:
        stones = input_file.read().strip()

    print("main:")
    print(count_stones(stones))
