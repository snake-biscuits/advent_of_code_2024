from typing import List


def sorted_checksum(disc_map: str, verbose: bool = False) -> int:
    file_id = 0
    filesystem = list()
    for i, char in enumerate(disc_map):
        count = int(char)
        if i % 2 == 0:  # data
            filesystem.extend([file_id] * count)
            file_id += 1
            last_data_index = len(filesystem) - 1
        else:  # free space
            filesystem.extend([None] * count)
    # sort
    assert None in filesystem
    first_none = filesystem.index(None)
    while first_none < last_data_index:
        file_id = filesystem[last_data_index]
        if file_id is not None:
            filesystem[first_none] = file_id
            filesystem[last_data_index] = None
        last_data_index -= 1
        first_none = filesystem.index(None)
        if verbose:
            print("".join([
                str(file_id) if file_id is not None else "."
                for file_id in filesystem]))
    return sum(
        i * file_id
        for i, file_id in enumerate(filesystem)
        if file_id is not None)


if __name__ == "__main__":
    test_disk_map = "2333133121414131402"

    print("\nexample:")
    print(sorted_checksum(test_disk_map, verbose=True))
    # expected output:
    # -- 00...111...2...333.44.5555.6666.777.888899
    # -- 009..111...2...333.44.5555.6666.777.88889.
    # -- 0099.111...2...333.44.5555.6666.777.8888..
    # -- 00998111...2...333.44.5555.6666.777.888...
    # -- 009981118..2...333.44.5555.6666.777.88....
    # -- 0099811188.2...333.44.5555.6666.777.8.....
    # -- 009981118882...333.44.5555.6666.777.......
    # -- 0099811188827..333.44.5555.6666.77........
    # -- 00998111888277.333.44.5555.6666.7.........
    # -- 009981118882777333.44.5555.6666...........
    # -- 009981118882777333644.5555.666............
    # -- 00998111888277733364465555.66.............
    # -- 0099811188827773336446555566..............
    # -- 1928

    with open("disk_map.txt") as input_file:
        disk_map = input_file.read().strip()

    print("\nmain:")
    print(sorted_checksum(disk_map))
