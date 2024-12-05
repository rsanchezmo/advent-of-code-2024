import time
import re


def parse_input(file: str):
    with open(file, 'r') as f:
        lines = f.readlines()


    ordering_rules = {}
    updates = []

    pattern = r"^(\d{1,2})\|(\d{1,2})$"
    for line in lines:
        match = re.match(pattern, line)
        if match:
            left, right = match.groups()
            ordering_rules.setdefault(left, set()).add(right)
        else:
            if line == '\n':
                continue
            updates.append(line.strip().split(','))


    return ordering_rules, updates



def part_a(file: str)  -> int:
    ordering_rules, updates = parse_input(file)
    
    sum = 0
    for update in updates:
        valid = True
        seen_set = set()
        for idx in range(1, len(update)):
            seen_set.add(update[idx-1])
            to_check = ordering_rules.get(update[idx], None)
            if to_check is None:
                continue
            if seen_set & to_check:
                valid = False
                break

        if valid:
            sum += int(update[len(update)//2]) 

    return sum     


def part_b(file: str) -> int:
    ordering_rules, updates = parse_input(file)

    sum = 0
    for update in updates:
        valid = False
        seen_set = set()
        for idx in range(1, len(update)):
            seen_set.add(update[idx-1])
            to_check = ordering_rules.get(update[idx], None)
            if to_check is None:
                continue
            if seen_set & to_check:
                valid = True
                break

        if valid:
            ordered = []
            visited = set()

            for number in reversed(update):
                if number not in visited:
                    visit(number, visited, ordering_rules, ordered, update)
            sum += int(ordered[len(ordered)//2]) 

    return sum     


def visit(number, visited, ordering_rules, ordered, update):
    if visit in visited:
        return
    
    for prev_number in ordering_rules.get(number, {}):
        if prev_number in update and prev_number not in visited:
            visit(prev_number, visited, ordering_rules, ordered, update)

    if number not in visited:
        visited.add(number)
        ordered.append(number)


if __name__ == '__main__':

    file = './05/input.txt'

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