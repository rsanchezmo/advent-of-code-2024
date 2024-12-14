import time
import re


def parse_input(file: str) -> list:
    with open(file, 'r') as f:
        lines = f.readlines()

    robots = []
    regex = r'p=(\d+),(\d+)\s*v=(-?\d+),(-?\d+)'
    for line in lines:
        match = re.search(regex, line)
        x, y, vx, vy = map(int, match.groups())
        robots.append({'p': [x, y], 'v': [vx, vy]})
    
    return robots

def part_a(file: str, map_rows: int = 103, map_cols: int = 101, moves: int = 100)  -> int:
    robots = parse_input(file)

    quadrants = {'upright': 0, 'upleft': 0, 'downright': 0, 'downleft': 0}
    for robot in robots:
        robot['p'][0] = (robot['p'][0] + robot['v'][0] * moves) % map_cols
        robot['p'][1] = (robot['p'][1] + robot['v'][1] * moves) % map_rows

        if robot['p'][0] < map_cols // 2 and robot['p'][1] < map_rows // 2:
            quadrants['upleft'] += 1
        elif robot['p'][0] < map_cols // 2 and robot['p'][1] > map_rows // 2:
            quadrants['downleft'] += 1
        elif robot['p'][0] > map_cols // 2 and robot['p'][1] < map_rows // 2:
            quadrants['upright'] += 1
        elif robot['p'][0] > map_cols // 2 and robot['p'][1] > map_rows // 2:
            quadrants['downright'] += 1

    return quadrants['upleft'] * quadrants['downright'] * quadrants['upright'] * quadrants['downleft']

def part_b(file: str, map_rows: int = 103, map_cols: int = 101)  -> int:
    robots = parse_input(file)
    
    seconds = 0
    while True:
        seconds += 1
        unique_locations = set()
        for robot in robots:
            new_col = (robot['p'][0] + seconds * robot['v'][0]) % map_cols
            new_row = (robot['p'][1] + seconds * robot['v'][1]) % map_rows

            unique_locations.add((new_col, new_row))

        if len(unique_locations) == len(robots):    
            map = [[' ' for _ in range(map_cols)] for _ in range(map_rows)]
            for location in unique_locations:
                map[location[1]][location[0]] = '#'
            print('\n'.join([''.join(row) for row in map]))
            print(f'Seconds: {seconds}')

            # THE WORKAROUND IS JUST TO PRINT THE GRID AND SEE IF THE CHRISTMAS TREE APPEARS (ONLY WHEN EVERY ROBOT IS AT UNIQUE POSITION, this is not intuitive, it is just a guess I read)
            # WE COULD ALSO PRINT THE GRID ONLY WHEN SEEING ####### (7 consecutive #) IN A ROW FOR INSTANCE UNTIL WE SAW THE CHRISTMAS TREE, EVERYONE TRIED SIMILAR STRATEGIES.

    return None

if __name__ == '__main__':

    file = './14/input.txt'

    init_t = time.perf_counter()
    part_a_sol = part_a(file, map_rows=103, map_cols=101, moves=100)
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