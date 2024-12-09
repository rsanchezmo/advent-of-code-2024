import time
import copy

def parse_input(file: str):
    with open(file, 'r') as f:
        lines = f.readlines()
    
    map = {}  # {block_idx: (n_blocks, free_space, [appended])}
    line = lines[0].strip()

    block_counter = 0
    for i in range(0, len(line), 2):
        n_blocks = int(line[i])
        free_space = int(line[i+1]) if i+1 < len(line) else 0
        
        map[block_counter] = [n_blocks, free_space, []]

        block_counter += 1
            
    return map


def part_a(file: str)  -> int:
    map = parse_input(file)
    
    right_idx = len(map) - 1
    left_idx = 0

    filesystem = [0] * map[0][0]
    while left_idx < right_idx:
        left_space = map[left_idx][1]

        if left_space == 0:
            left_idx += 1
            filesystem += [left_idx] * map[left_idx][0]
            continue

        right_blocks = map[right_idx][0]

        if right_blocks == 0:
            right_idx -= 1
            continue

        n_blocks = min(left_space, right_blocks)
        map[left_idx][1] -= n_blocks
        map[right_idx][0] -= n_blocks

        filesystem += [right_idx] * n_blocks
    
    return sum(value * i for i, value in enumerate(filesystem))



def part_b(file: str) -> int:
    map = parse_input(file)
    orig_map = copy.deepcopy(map)
    
    right_idx = len(map) - 1
    left_idx = 0

    while left_idx < right_idx:
        left_space = map[left_idx][1]

        if left_space == 0:
            left_idx += 1
            continue

        right_blocks = map[right_idx][0]

        if right_blocks > left_space:
            # no left space, lets try with next block
            left_idx += 1
            if left_idx >= right_idx:
                left_idx = 0
                # move to the next right block
                right_idx -= 1
            continue

        # provide the new global index
        map[left_idx][-1].append(right_idx)
        #map[right_idx][-1] = None  # I have moved it

        # reduce the available space in the left
        map[left_idx][1] -= right_blocks
        # map[right_idx][1] = 0  # no more free space in the right

        # move to the next right block
        right_idx -= 1


    filesystem = ['.'] * sum([orig_map[i][0] + orig_map[i][1] for i in map.keys()])
    global_idx = 0
    has_moved = set()
    for i in range(len(map)):
        if i not in has_moved:
            filesystem[global_idx : global_idx + orig_map[i][0]] = [str(i)] * orig_map[i][0]
            init_idx = global_idx + orig_map[i][0]
        else:
            init_idx = global_idx + orig_map[i][0]  # I have moved it, it will only have appended higher indices, so we have to move the pointer with the n_blocks

        if len(map[i][-1]) > 0:
            for appended in map[i][-1]:
                has_moved.add(appended)
                filesystem[init_idx : init_idx + orig_map[appended][0]] = [str(appended)] * orig_map[appended][0]
                init_idx += orig_map[appended][0]
            global_idx = init_idx + map[i][1]  # free spaces
        else:
            if i not in has_moved:
                global_idx += orig_map[i][1] + map[i][0]  # free spaces + previous blocks
            else:
                global_idx += map[i][1] # previous blocks
    
    print(''.join(filesystem))

    checksum = sum([int(value) * i if value != '.' else 0 for i, value in enumerate(filesystem)])
    return checksum

if __name__ == '__main__':

    file = './09/input.txt'

    init_t = time.perf_counter()
    part_a_sol = part_a(file)
    end_t = time.perf_counter()
    elapsed = end_t - init_t
    print(f'\033[32mPart A: {part_a_sol}')
    print(f'Part A: {elapsed * 1e3:.2f} ms\033[0m')

    init_t = time.perf_counter()
    part_b_sol = part_b(file)
    end_t = time.perf_counter()
    elapsed = end_t - init_t
    print(f'\033[34mPart B: {part_b_sol}')
    print(f'Part B: {elapsed * 1e3:.2f} ms\033[0m')