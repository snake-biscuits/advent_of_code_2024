from typing import Dict, List, Tuple, Union


def make_filesystem(file_dict: Dict[int, Tuple[int, int]]) -> List[Union[int, None]]:
    filesystem = list()
    for file_id in sorted(file_dict, key=file_dict.get):
        offset, length = file_dict[file_id]
        if len(filesystem) < offset:
            count = offset - len(filesystem)
            filesystem.extend([None] * count)
        filesystem.extend([file_id] * length)
    return filesystem


def sorted_checksum(disc_map: str, verbose: bool = False) -> int:
    file = list()
    # ^ [(offset, length)]
    free = list()
    # ^ [(offset, length)]
    cursor = 0
    for i, char in enumerate(disc_map):
        count = int(char)
        if i % 2 == 0:  # data
            file.append((cursor, count))
        else:  # free space
            free.append((cursor, count))
        cursor += count
    file_dict = {
        i: (offset, length)
        for i, (offset, length) in enumerate(file)}
    # ^ {file_id: (offset, length)}
    # sort
    if verbose:
        filesystem = make_filesystem(file_dict)
        print("".join([
            str(file_id) if file_id is not None else "."
            for file_id in filesystem]))
    file_id = max(file_dict)
    while file_id >= 0:
        offset, length = file_dict[file_id]
        for i, (free_offset, free_length) in enumerate(free):
            if free_offset > offset:
                break
            if length <= free_length:
                offset = free_offset
                free_offset += length
                free_length -= length
                file_dict[file_id] = (offset, length)
                if verbose:
                    filesystem = make_filesystem(file_dict)
                    # NOTE: don't have enough characters to debug a big filesystem
                    print("".join([
                        str(file_id) if file_id is not None else "."
                        for file_id in filesystem]))
                if free_length > 0:
                    free[i] = (free_offset, free_length)
                else:  # no longer free
                    free.pop(i)
                break
        file_id -= 1
    filesystem = make_filesystem(file_dict)
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
    # -- 0099.111...2...333.44.5555.6666.777.8888..
    # -- 0099.1117772...333.44.5555.6666.....8888..
    # -- 0099.111777244.333....5555.6666.....8888..
    # -- 00992111777.44.333....5555.6666.....8888..
    # -- 2858

    with open("disk_map.txt") as input_file:
        disk_map = input_file.read().strip()

    print("\nmain:")
    print(sorted_checksum(disk_map))
