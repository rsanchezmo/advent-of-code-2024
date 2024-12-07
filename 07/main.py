import time


def parse_input(file: str):
    with open(file, 'r') as f:
        lines = f.readlines()
    
    equations = {}
    for line in lines:
        line = line.strip()

        test_value = line.split(': ')[0]
        values = list(map(int, line.split(': ')[1].split(' ')))
        equations[int(test_value)] = values

    return equations


def is_valid_eq(test, numbers, operator, accum = 0):

    accum = eval(f"{accum}{operator}{numbers[0]}")

    if len(numbers) - 1 == 0:
        if accum == test:
            return True
        return False
    else:
        if accum > test:
            return False
        
        return is_valid_eq(test, numbers[1:], operator='+', accum=accum) or is_valid_eq(test, numbers[1:], operator='*', accum=accum)


def part_a(file: str)  -> int:
    equations = parse_input(file) 

    valid_eq = 0
    for test, numbers in equations.items():
        if is_valid_eq(test, numbers, operator='+', accum=0):
            valid_eq += test

    return valid_eq

    
def new_is_valid_eq(test, numbers, operator, accum = 0):
    accum = eval(f"{accum}{operator}{numbers[0]}")

    if len(numbers) - 1 == 0:
        if accum == test:
            return True
        return False
    else:
        if accum > test:
            return False
        
        return new_is_valid_eq(test, numbers[1:], operator='+', accum=accum) or new_is_valid_eq(test, numbers[1:], operator='*', accum=accum) or new_is_valid_eq(test, numbers[1:], operator='', accum=accum)
    

def part_b(file: str) -> int:
    equations = parse_input(file) 

    valid_eq = 0
    for test, numbers in equations.items():
        if new_is_valid_eq(test, numbers, operator='+', accum=0):
            valid_eq += test

    return valid_eq


if __name__ == '__main__':

    file = './07/input.txt'

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