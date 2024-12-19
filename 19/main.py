import time
from functools import lru_cache


def parse_input(file: str) -> list:
    with open(file, 'r') as f:
        lines = f.readlines()

    get_patterns = True
    designs = []
    for line in lines:
        line = line.strip()
        if get_patterns:
            patterns = tuple(sorted(line.split(', '), key=len, reverse=True))
            get_patterns = False

        else:
            if line == '':
                continue
            designs.append(line)

    return patterns, designs



@lru_cache(maxsize=None)
def search(pattern, towels):
    design_count = 0
    for towel in towels:
        if pattern == towel:
            design_count += 1

        if pattern.startswith(towel):
            design_count += search(pattern.removeprefix(towel), towels)

    return design_count


def part_a(file: str)  -> int:
    towels, patterns = parse_input(file)

    valid_designs = 0
    for pattern in patterns:
        valid_designs += (search(pattern, towels) > 0)

    return valid_designs

def part_b(file: str)  -> int:
    towels, patterns = parse_input(file)

    valid_designs = 0
    for pattern in patterns:
        valid_designs += search(pattern, towels)

    return valid_designs

if __name__ == '__main__':

    file = './19/input.txt'

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