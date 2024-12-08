import time
import copy


MOVES = {
    0: (-1, 0),  # up
    1: (0, 1),   # right
    2: (1, 0),   # down
    3: (0, -1),  # left
}


def parse_input(file: str):
    with open(file, 'r') as f:
        lines = f.readlines()
    
    map = []
    orig = None
    for row, line in enumerate(lines):
        map.append(line.strip())

        try:
            index = line.index('^')
        except:
            index = None

        if index:
            orig = (row, index, 0)  # row, col, ori
    return map, orig

def get_unique_positions(map, orig):
    unique_positions = {orig[:2]}
    unique_positions_dir = {orig}

    prev_pos = orig
    while True:
        row, col, ori = prev_pos

        row += MOVES[ori][0]
        col += MOVES[ori][1]

        if row < 0 or row >= len(map) or col < 0 or col >= len(map[0]):
            break

        while map[row][col] == '#':
            ori = (ori + 1) % 4
            row, col, _ = prev_pos
            #row += MOVES[ori][0]
            #col += MOVES[ori][1]

        prev_pos = (row, col, ori)
        unique_positions.add(prev_pos[:2])
        unique_positions_dir.add(prev_pos)

    return unique_positions, unique_positions_dir


def part_a(file: str)  -> int:
    map, orig = parse_input(file) 

    unique_positions, _ = get_unique_positions(map, orig)

    return len(unique_positions)



def check_loop(grid_map, orig):
    seen = set()

    guard_pos = orig[:2]
    guard_dir = orig[2]

    while True:

        guard_pos_dir = (guard_pos[0], guard_pos[1], guard_dir)
        if guard_pos_dir in seen:
            return True
        
        seen.add(guard_pos_dir)

        dx, dy = MOVES[guard_dir]
        new_row, new_col = guard_pos[0] + dx, guard_pos[1] + dy

        if new_row not in range(len(grid_map)) or new_col not in range(len(grid_map[0])):
            return False

        if grid_map[new_row][new_col] == "#":
            guard_dir = (guard_dir + 1) % 4
            continue
        
        guard_pos = (new_row, new_col)


def part_b(file: str) -> int:
    map, orig = parse_input(file)

    unique_positions, _ = get_unique_positions(map, orig)    

    loop_count = 0
    for pos in unique_positions:
        if pos == orig[:2]:
            continue
        
        map_reformat = [list(line) for line in map]
        map_copy = copy.deepcopy(map_reformat)
        map_copy[pos[0]][pos[1]] = "#"

        if check_loop(map_copy, orig):
            loop_count += 1
    
    return loop_count
    


if __name__ == '__main__':

    file = './06/input.txt'

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