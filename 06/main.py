import time

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


def part_b(file: str) -> int:
    map, orig = parse_input(file)

    _, unique_positions_dir = get_unique_positions(map, orig)
    obstructions = set()

    for orig in unique_positions_dir:
        row, col, ori = orig
        obs_candidate = (row + MOVES[ori][0], col + MOVES[ori][1], ori)

        if not (0 <= obs_candidate[0] < len(map) and 0 <= obs_candidate[1] < len(map[0])) or map[obs_candidate[0]][obs_candidate[1]] == '#':
            continue

        # try putting an obstacle, if the next move is a previous position
        new_ori = (ori + 1) % 4
        new_row = row #+ MOVES[new_ori][0]
        new_col = col #+ MOVES[new_ori][1]

        prev_pos = (new_row, new_col, new_ori)

        # print('Origin: ', orig, 'Obs candidate: ', obs_candidate, 'Next pos:', prev_pos)
        
        loop_poses = {orig}
        while True: # move until finding a loop, or escaping the initial area :)
            row, col, ori = prev_pos
            if prev_pos in loop_poses:
                obstructions.add(obs_candidate[:2])
                break

            loop_poses.add(prev_pos)

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

    print(obstructions)

    return len(obstructions)


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