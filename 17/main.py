import time
import copy
from functools import lru_cache



def parse_input(file: str) -> list:
    with open(file, 'r') as f:
        lines = f.readlines()

    registers = {}
    ops = []
    for line in lines:
        line = line.strip()

        if 'Register A:' in line:
            registers['A'] = int(line.split(': ')[1])
        elif 'Register B:' in line:
            registers['B'] = int(line.split(': ')[1])
        elif 'Register C:' in line:
            registers['C'] = int(line.split(': ')[1])
        elif 'Program:' in line:
            ops = (line.split(': ')[1]).split(',')

    return registers, ops

def part_a(file: str)  -> int:
    registers, ops = parse_input(file)

    COMBO = {
        '0': lambda : 0,
        '1': lambda : 1,
        '2': lambda : 2,
        '3': lambda : 3,
        '4': lambda : registers['A'],
        '5': lambda : registers['B'],
        '6': lambda : registers['C']
    }

    idx = 0
    outputs = []
    while idx < len(ops) - 1:
        opcode = ops[idx]
        operand = ops[idx + 1]

        match opcode:
            case '0':
                numerator = registers['A']
                denominator = 2  ** COMBO[operand]()
                result = numerator // denominator
                registers['A'] = result

            case '1':
                result = registers['B'] ^ int(operand)
                registers['B'] = result
            
            case '2':
                result = COMBO[operand]() % 8
                registers['B'] = result

            case '3':
                if registers['A'] > 0:
                    idx = int(operand)
                    continue
            
            case '4':
                result = registers['C'] ^ registers['B']
                registers['B'] = result

            case '5':
                outputs.append(str(COMBO[operand]() % 8))

            case '6':
                numerator = registers['A']
                denominator = 2  ** COMBO[operand]()
                result = numerator // denominator
                registers['B'] = result

            case '7':
                numerator = registers['A']
                denominator = 2  ** COMBO[operand]()
                result = numerator // denominator
                registers['C'] = result

        idx += 2

    return ','.join(outputs)



# @lru_cache(maxsize=None)
def get_combo(operand: str, a_register: int, b_register: int, c_register: int) -> int:
    if operand == '0':
        return 0
    elif operand == '1':
        return 1
    elif operand == '2':
        return 2
    elif operand == '3':
        return 3
    elif operand == '4':
        return a_register
    elif operand == '5':
        return b_register
    elif operand == '6':
        return c_register
    
    return -1
            

#@lru_cache(maxsize=None)
def apply_opcode(opcode: str, operand: str, register_a: int, register_b: int, register_c: int, combo: int) -> tuple:
    if opcode == '0':
            numerator = register_a
            denominator = 2  ** combo
            result = numerator // denominator
            return result, register_b, register_c, None, None
    elif opcode == '1':
            result = register_b ^ int(operand)
            return register_a, result, register_c, None, None
    elif opcode == '2':
            result = combo % 8
            return register_a, result, register_c, None, None

    elif opcode == '3': 
            if register_a > 0:
                return register_a, register_b, register_c, int(operand), None
            return register_a, register_b, register_c, None, None

    elif opcode == '4':
            result = register_c ^ register_b
            return register_a, result, register_c, None, None

    elif opcode == '5':
            new_output = combo % 8
            return register_a, register_b, register_c, None, new_output

    elif opcode == '6':
            numerator = register_a
            denominator = 2  ** combo
            result = numerator // denominator
            return register_a, result, register_c, None, None

    elif opcode == '7':
            numerator = register_a
            denominator = 2  ** combo
            result = numerator // denominator
            return register_a, register_b, result, None, None

    return -1, -1, -1, None, None


def part_b(file: str)  -> int:
    original_registers, ops = parse_input(file)
    

    expected_output = ops
    print(expected_output)

    a_candidate = 1_000_000_000
    while True:
        a_candidate += 1
        registers_a, registers_b, registers_c = original_registers['A'], original_registers['B'], original_registers['C']
        registers_a = a_candidate

        print(f'a_candidate: {a_candidate}') if a_candidate % 100_000 == 0 else None
        
        idx = 0
        outputs = []
        escape = False
        while idx < len(ops) - 1:
            opcode = ops[idx]
            operand = ops[idx + 1]
            combo = get_combo(operand, registers_a, registers_b, registers_c)

            registers_a, registers_b, registers_c, next_idx, new_output = apply_opcode(opcode, operand, registers_a, registers_b, registers_c, combo)
            if next_idx is not None:
                idx = next_idx
                continue

            if new_output is not None:
                outputs.append(str(new_output))
                print('new_output:', new_output)
                for idx_ in range(len(outputs)):
                    if len(outputs) > len(expected_output) or outputs[idx_] != expected_output[idx_]:  
                        escape = True
                        break

            idx += 2

            if escape:
                break

        if outputs == expected_output:
            print(f'a_candidate: {a_candidate} produced the expected output: {outputs}')
            return a_candidate

if __name__ == '__main__':

    file = './17/example_2.txt'

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