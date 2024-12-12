import time
from collections import defaultdict
from functools import lru_cache

MOVES = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1)
}


def parse_input(file: str):
    with open(file, 'r') as f:
        lines = f.readlines()
    
    return [line.strip() for line in lines]

def part_a(file: str)  -> int:
    farm = parse_input(file)

    def get_region(row, col, region_set):
        region = farm[row][col]
        perimeter = 0
        area = 1
        for move in MOVES:
            new_row, new_col = row + MOVES[move][0], col + MOVES[move][1]
            if new_row < 0 or new_row >= len(farm) or new_col < 0 or new_col >= len(farm[0]) or farm[new_row][new_col] != region:
                perimeter += 1
                continue

            if (new_row, new_col) in region_set:
                continue

            region_set.add((new_row, new_col))
            new_perimeter, new_area = get_region(new_row, new_col, region_set)
            perimeter += new_perimeter
            area += new_area

        return perimeter, area
    
    already_seen = set()
    total_price = 0
    for row in range(len(farm)):
        for col in range(len(farm[0])):
            if (row, col) in already_seen:
                continue
            
            region_set = {(row, col)}
            perimeter, area = get_region(row, col, region_set)
            total_price += area * perimeter

            already_seen.update(region_set)

    return total_price

def part_b(file: str)  -> int:
    farm = parse_input(file)

    def get_region(row, col, region_set):
        region = farm[row][col]
        perimeter = 0
        area = 1
        for move in MOVES:
            new_row, new_col = row + MOVES[move][0], col + MOVES[move][1]
            if new_row < 0 or new_row >= len(farm) or new_col < 0 or new_col >= len(farm[0]) or farm[new_row][new_col] != region:
                perimeter += 1
                continue

            if (new_row, new_col) in region_set:
                continue

            region_set.add((new_row, new_col))
            new_perimeter, new_area = get_region(new_row, new_col, region_set)
            perimeter += new_perimeter
            area += new_area

        return perimeter, area
    
    # search for all regions
    already_seen = set()
    regions = []
    for row in range(len(farm)):
        for col in range(len(farm[0])):
            if (row, col) in already_seen:
                continue
            
            region_set = {(row, col)}
            _, area = get_region(row, col, region_set)
            regions.append((area, region_set))
            already_seen.update(region_set)

    total_price = 0
    for area, region_set in regions:
        # number of sides is the number of corners :)
        sides = 0
        for component in region_set:
            # up
            up_pose = (component[0] + MOVES['up'][0], component[1] + MOVES['up'][1])
            up_out = up_pose not in region_set

            # down
            down_pose = (component[0] + MOVES['down'][0], component[1] + MOVES['down'][1])
            down_out = down_pose not in region_set

            # left
            left_pose = (component[0] + MOVES['left'][0], component[1] + MOVES['left'][1])
            left_out = left_pose not in region_set

            # right
            right_pose = (component[0] + MOVES['right'][0], component[1] + MOVES['right'][1])
            right_out = right_pose not in region_set

            # diagonal
            up_left_pose = (component[0] + MOVES['up'][0] + MOVES['left'][0], component[1] + MOVES['up'][1] + MOVES['left'][1])
            up_left_out = up_left_pose not in region_set

            up_right_pose = (component[0] + MOVES['up'][0] + MOVES['right'][0], component[1] + MOVES['up'][1] + MOVES['right'][1])
            up_right_out = up_right_pose not in region_set

            down_left_pose = (component[0] + MOVES['down'][0] + MOVES['left'][0], component[1] + MOVES['down'][1] + MOVES['left'][1])
            down_left_out = down_left_pose not in region_set

            down_right_pose = (component[0] + MOVES['down'][0] + MOVES['right'][0], component[1] + MOVES['down'][1] + MOVES['right'][1])
            down_right_out = down_right_pose not in region_set

            # check how many corners do we have here (convex)
            sides += sum([up_out and left_out, up_out and right_out, down_out and left_out, down_out and right_out])

            # check how many corners do we have here (concave)
            sides += sum([down_out and not down_right_out, down_out and not down_left_out, up_out and not up_right_out, up_out and not up_left_out])

            # remove special cases where we have both a convex and concave corner
            sides -= sum([up_out and left_out and not up_left_out, up_out and right_out and not up_right_out, down_out and left_out and not down_left_out, down_out and right_out and not down_right_out])

        total_price += area * sides


    return total_price


if __name__ == '__main__':

    file = './12/input.txt'

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