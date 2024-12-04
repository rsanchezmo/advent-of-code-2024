import time


def parse_input(file: str):
    with open(file, 'r') as f:
        lines = f.readlines()

    map = [line.strip() for line in lines]
    
    return map


MOVES = {
    'up': (-1, 0),
    'upleft': (-1, -1),
    'upright': (-1, 1),
    'down': (1, 0),
    'downleft': (1, -1),
    'downright': (1, 1),
    'left': (0, -1),
    'right': (0, 1)
}

MOVES_DIAG = {
    'upleft': (-1, -1),
    'upright': (-1, 1),
    'downleft': (1, -1),
    'downright': (1, 1)
}



def are_any_mas(x: int, y: int, map: list) -> int:
    word_count = 0

    for move, delta in MOVES.items():
        found = True
        next_y = y
        next_x = x
        for letter in 'MAS':
            next_y = next_y + delta[0]
            next_x = next_x + delta[1]
            if next_y < 0 or next_x < 0 or next_y >= len(map) or next_x >= len(map[0]) or map[next_y][next_x] != letter:
                found = False
                break

        word_count += found

    return word_count


def part_a(file: str)  -> int:
    map = parse_input(file)

    word_count = 0
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == 'X':
                word_count += are_any_mas(x=x, y=y, map=map)

    return word_count


def is_an_x(x: int, y: int, map: list) -> int:

    upleft_val = None
    upright_val = None
    for move, delta in MOVES_DIAG.items():
        next_y = y + delta[0]
        next_x = x + delta[1]
        
        if next_y < 0 or next_x < 0 or next_y >= len(map) or next_x >= len(map[0]):
            return 0
        
        char = map[next_y][next_x]
        if char not in 'MS':
            return 0 

        if move == 'upleft': 
            upleft_val = char
            continue

        if move == 'upright':
            upright_val = char
            continue

        if move == 'downleft' and upright_val == char:
            return 0
        
        if move == 'downright' and upleft_val == char:
            return 0
            
    return 1

def part_b(file: str) -> int:
    map = parse_input(file)

    word_count = 0
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == 'A':
                word_count += is_an_x(x=x, y=y, map=map)

    return word_count


if __name__ == '__main__':

    file = './04/input.txt'

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