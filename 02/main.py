import time

def parse_input(file: str):
    with open(file, 'r') as f:
        lines = f.readlines()
    reports = [list(map(int, line.split(' '))) for line in lines]
    return reports

def is_safe_report(report):
    diff = report[0] - report[1]
    if abs(diff) > 3 or diff == 0:
        return False

    increasing = diff < 0

    for i in range(1, len(report)-1):
        diff = report[i] - report[i+1]
        if abs(diff) > 3 or diff == 0 or (increasing and diff > 0) or (not increasing and diff < 0):
            return False

    return True

def part_a(file: str)  -> int:
    reports = parse_input(file)

    safe_reports = 0
    for report in reports:
        if is_safe_report(report):
            safe_reports += 1

    return safe_reports

def part_b(file: str) -> int:
    reports = parse_input(file)
    safe_reports = 0
    for report in reports:
        for level_idx in range(len(report)):
            new_report = report[:level_idx] + report[level_idx+1:]
            if is_safe_report(new_report):
                safe_reports += 1
                break

    return safe_reports

if __name__ == '__main__':

    file = './02/input.txt'

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