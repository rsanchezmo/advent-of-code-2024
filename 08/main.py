import time
import re

def parse_input(file: str):
    with open(file, 'r') as f:
        lines = f.readlines()
    
    return [line.strip() for line in lines]


def part_a(file: str)  -> int:
    map = parse_input(file)
    
    freqs = {}

    for row_idx, row in enumerate(map):
        indices = [match.start() for match in re.finditer(r'[^.]', row)]
        for col in indices:
            freq = row[col]
            freqs[freq] = freqs.get(freq, []) + [(row_idx, col)]

    antinodes = set()
    for coords in freqs.values():
        if len(coords) == 1:
            continue

        for coord_idx in range(len(coords) - 1):
            for coord_idx_2 in range(coord_idx + 1, len(coords)):
                delta_row = coords[coord_idx_2][0] - coords[coord_idx][0]
                delta_col = coords[coord_idx_2][1] - coords[coord_idx][1]

                # there are two antinodes, one on either side of them, so must compute the direction and add to one side and to another
                first_candidate = (coords[coord_idx][0] - delta_row, coords[coord_idx][1] - delta_col)
                second_candidate = (coords[coord_idx_2][0] + delta_row, coords[coord_idx_2][1] + delta_col)

                if 0 <= first_candidate[0] < len(map) and 0 <= first_candidate[1] < len(map[0]):
                    antinodes.add(first_candidate)

                if 0 <= second_candidate[0] < len(map) and 0 <= second_candidate[1] < len(map[0]):
                    antinodes.add(second_candidate)

    return len(antinodes)


def part_b(file: str) -> int:
    map = parse_input(file) 

    freqs = {}

    for row_idx, row in enumerate(map):
        indices = [match.start() for match in re.finditer(r'[^.]', row)]
        for col in indices:
            freq = row[col]
            freqs[freq] = freqs.get(freq, []) + [(row_idx, col)]

    antinodes = set()
    for coords in freqs.values():
        if len(coords) == 1:
            continue

        for coord_idx in range(len(coords) - 1):
            for coord_idx_2 in range(coord_idx + 1, len(coords)):
                delta_row = coords[coord_idx_2][0] - coords[coord_idx][0]
                delta_col = coords[coord_idx_2][1] - coords[coord_idx][1]

                # side 1
                idx = 0
                while True:
                    first_candidate = (coords[coord_idx][0] - idx * delta_row, coords[coord_idx][1] - idx * delta_col)
                    if 0 <= first_candidate[0] < len(map) and 0 <= first_candidate[1] < len(map[0]):
                        antinodes.add(first_candidate)
                    else:
                        break
                    
                    idx += 1
                
                # side 2
                idx = 0
                while True:
                    second_candidate = (coords[coord_idx_2][0] + idx * delta_row, coords[coord_idx_2][1] + idx * delta_col)
                    if 0 <= second_candidate[0] < len(map) and 0 <= second_candidate[1] < len(map[0]):
                        antinodes.add(second_candidate)
                    else:
                        break
                    
                    idx += 1

    return len(antinodes)

if __name__ == '__main__':

    file = './08/input.txt'

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