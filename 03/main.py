import time
import re


def parse_input(file: str):
    with open(file, 'r') as f:
        text = f.read()
    return text

def part_a(file: str)  -> int:
    text = parse_input(file)
    regex = r'mul\(([1-9][0-9]{0,2}),([1-9][0-9]{0,2})\)'  # find the mul (I use 2 groups, the x and the y)
    matches = re.findall(regex, text)

    sum = 0
    for x, y in matches:
        sum += int(x) * int(y)
    return sum

    

def part_b(file: str) -> int:
    text =  parse_input(file)
    regex = r'mul\(([1-9][0-9]{0,2}),([1-9][0-9]{0,2})\)|((?:do|don\'t)\(\))'  # find the mul or the enablers ( I use 3 groups, the x, y and the enabler)
    matches = re.findall(regex, text)

    sum = 0
    enabled = True
    for x, y, order in matches:
        if order == "do()":
            enabled = True
        if order == "don't()":
            enabled = False
        if x != '' and enabled:
            sum += int(x) * int(y)
    return sum

if __name__ == '__main__':

    file = './03/input.txt'

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