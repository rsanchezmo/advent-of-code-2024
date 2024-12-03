import time

def parse_input(file: str):
    with open(file, 'r') as f:
        lines = f.readlines()

    left_array = []
    right_array = []
    for line in lines:
        left, right = line.split('   ')
        left_array.append(int(left))
        right_array.append(int(right))

    return left_array, right_array

def part_a(file: str)  -> int:
    left_array, right_array = parse_input(file)

    left_array = sorted(left_array)
    right_array = sorted(right_array) 
    accum = 0
    for i in range(len(left_array)):
        accum += abs(right_array[i] - left_array[i])
    
    return accum

def part_b(file: str) -> int:
    left_array, right_array = parse_input(file)
    frecuency_right = {}
    for number in right_array:
        frecuency_right[number] = frecuency_right.get(number, 0) + 1

    score = 0
    for number in left_array:
        score += number * frecuency_right.get(number, 0)

    return score


if __name__ == '__main__':

    file = './01/input.txt'

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