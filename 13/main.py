import time
import re


def parse_input(file: str, add_to_P = 0) -> list:
    with open(file, 'r') as f:
        lines = f.readlines()
    
    challenges = []
    next_value = 'A'
    challenge = {}
    for line in lines:
        line = line.strip()
        if line == '':
            continue

        if next_value == 'A':
            regex = r"X\+(\d+),\s*Y\+(\d+)"
            match = re.search(regex, line)
            X, Y = match.groups()
            challenge['A'] = (int(X), int(Y))
            next_value = 'B'
            continue
        
        if next_value == 'B':
            regex = r"X\+(\d+),\s*Y\+(\d+)"
            match = re.search(regex, line)
            X, Y = match.groups()
            challenge['B'] = (int(X), int(Y))
            next_value = 'P'
            continue

        if next_value == 'P':
            regex = r"X\=(\d+),\s*Y\=(\d+)"
            match = re.search(regex, line)
            X, Y = match.groups()
            challenge['P'] = (int(X) + add_to_P, int(Y) + add_to_P)
            next_value = 'A'
            challenges.append(challenge)
            challenge = {}
            continue

    return challenges


def part_a(file: str, add_to_P = 0)  -> int:
    challenges = parse_input(file, add_to_P)

    total_tokens = 0
    for challenge in challenges:
        # cramer's rule
        determinant = challenge['A'][0] * challenge['B'][1] - challenge['A'][1] * challenge['B'][0]

        if determinant == 0:
            continue

        a_presses = (challenge['P'][0] * challenge['B'][1] - challenge['P'][1] * challenge['B'][0]) / determinant
        b_presses = (challenge['A'][0] * challenge['P'][1] - challenge['A'][1] * challenge['P'][0]) / determinant
        
        if a_presses < 0 or b_presses < 0 or a_presses % 1 != 0 or b_presses % 1 != 0:
            # if < 0 solution or not integer solution
            continue

        a_presses = int(a_presses)
        b_presses = int(b_presses)
        tokens = a_presses * 3 + b_presses
        total_tokens += tokens 

    return total_tokens


if __name__ == '__main__':

    file = './13/input.txt'

    init_t = time.perf_counter()
    part_a_sol = part_a(file, add_to_P=0)
    end_t = time.perf_counter()
    elapsed = end_t - init_t
    print(f'\033[32mPart A: {part_a_sol}')
    print(f'Part A: {elapsed * 1e3:.2f} ms\033[0m')

    init_t = time.perf_counter()
    part_b_sol = part_a(file, add_to_P=10000000000000)
    end_t = time.perf_counter()
    elapsed = end_t - init_t
    print(f'\033[34mPart B: {part_b_sol}')
    print(f'Part B: {elapsed * 1e3:.2f} ms\033[0m')