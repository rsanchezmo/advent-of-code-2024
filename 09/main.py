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
        right_blocks = map[right_idx][0]

        if right_blocks > left_space:
            # no left space, lets try with next block
            left_idx += 1
            if left_idx >= right_idx:
                left_idx = 0
                right_idx -= 1
            continue

        # append the right block to the left
        map[left_idx][-1].append(right_idx)
        # reduce the available space in the left
        map[left_idx][1] -= right_blocks

        # move to the next right block
        right_idx -= 1
        left_idx = 0


    filesystem = ['.'] * sum([orig_map[i][0] + orig_map[i][1] for i in map.keys()])

    init_idx = 0
    has_moved = set()
    for i in range(len(map)):
        n_blocks = map[i][0]
        free_space = map[i][1]
        orig_free_space = orig_map[i][1]
        total_space = n_blocks + orig_free_space
        appended_files = map[i][-1]

        if i not in has_moved:
            # we should draw the blocks on the current file
            filesystem[init_idx : init_idx + n_blocks] = [str(i)] * n_blocks
        
        init_idx += n_blocks  # we should account the blocks of that file

        if appended_files:  # if we have appended blocks
            for appended in appended_files:
                has_moved.add(appended)  # record the already moved blocks
                appended_blocks = map[appended][0]
                filesystem[init_idx : init_idx + appended_blocks] = [str(appended)] * appended_blocks
                init_idx += appended_blocks  # we should account the blocks of that file
            
        init_idx += free_space  # free spaces, it may not be entirely filled
    
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