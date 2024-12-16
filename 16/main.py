import time
from dataclasses import dataclass
import heapq
from pprint import pprint


MOVES = {
    0: (1, 0),   # right
    2: (-1, 0),  # left
    3: (0, -1),  # up
    1: (0, 1),   # down
}


def parse_input(file: str) -> list:
    with open(file, 'r') as f:
        lines = f.readlines()

    map = []
    for line in lines:
        line = line.strip()
        if 'E' in line:
            goal = (line.index('E'), len(map))
        if 'S' in line:
            orig = (line.index('S'), len(map))
        
        map.append(list(line))

    return map, orig, goal


@dataclass
class Node:
    pos: tuple
    ori: int  # 0: east, 1: south, 2: west, 3: north
    cost: int
    parent: 'Node' = None

    def __lt__(self, other):
        return self.cost < other.cost

def heuristic(node: Node, goal: Node) -> int:
    return abs(node.pos[0] - goal.pos[0]) + abs(node.pos[1] - goal.pos[1])


def part_a(file: str)  -> int:
    map, orig, goal = parse_input(file)

    orig_node = Node(pos=orig, ori=0, cost=0)
    goal_node = Node(pos=goal, ori=0, cost=0)
    
    # a-star
    open_list = []
    heapq.heappush(open_list, (heuristic(orig_node, goal_node), orig_node))
    visited = set()

    while open_list:
        _, current_node = heapq.heappop(open_list)

        if current_node.pos == goal_node.pos:
            return current_node.cost

        for i in range(4):
            delta_x, delta_y = MOVES[i]
            new_x = current_node.pos[0] + delta_x
            new_y = current_node.pos[1] + delta_y

            if new_x < 0 or new_x >= len(map[0]) or new_y < 0 or new_y >= len(map) or map[new_y][new_x] == '#':
                continue

            changes_in_ori = min(abs(current_node.ori - i), 4 - abs(current_node.ori - i))
            cost = current_node.cost + 1 + 1_000 * changes_in_ori
            new_node = Node(pos=(new_x, new_y), ori=i, cost=cost, parent=current_node)
            
            if new_node.pos in visited:
                continue

            priority = cost + heuristic(new_node, goal_node)
            heapq.heappush(open_list, (priority, new_node))

        visited.add(current_node.pos)

    return -1


def a_star(map, orig, goal):
    orig_node = Node(pos=orig, ori=0, cost=0)
    goal_node = Node(pos=goal, ori=0, cost=0)
    
    # a-star
    open_list = []
    heapq.heappush(open_list, (heuristic(orig_node, goal_node), orig_node))
    visited = set()

    while open_list:
        _, current_node = heapq.heappop(open_list)

        if current_node.pos == goal_node.pos:
            path = []
            cost = current_node.cost
            while current_node:
                path.append(current_node.pos)
                current_node = current_node.parent
            return path[::-1], cost

        for i in range(4):
            delta_x, delta_y = MOVES[i]
            new_x = current_node.pos[0] + delta_x
            new_y = current_node.pos[1] + delta_y

            if new_x < 0 or new_x >= len(map[0]) or new_y < 0 or new_y >= len(map) or map[new_y][new_x] == '#':
                continue

            changes_in_ori = min(abs(current_node.ori - i), 4 - abs(current_node.ori - i))
            cost = current_node.cost + 1 + 1_000 * changes_in_ori
            new_node = Node(pos=(new_x, new_y), ori=i, cost=cost, parent=current_node)

            if new_node.pos in visited:
                continue

            priority = cost + heuristic(new_node, goal_node)
            heapq.heappush(open_list, (priority, new_node))

        visited.add(current_node.pos)

    return None, None

def part_b(file: str)  -> int:
    map, orig, goal = parse_input(file)

    main_path, cost = a_star(map, orig, goal)
    tiles = set(main_path)
    tiles_revisited = set()
    while tiles_revisited != tiles:
        intersection = tiles - tiles_revisited
        for node in intersection:
            tiles_revisited.add(node)
            if node == orig or node == goal:
                continue

            # try another a_star with a # on this current point to try to find another path
            map[node[1]][node[0]] = '#'
            new_path, new_cost = a_star(map, orig, goal, return_if_cost_exceeds=cost)
            if new_path and new_cost == cost:
                tiles.update(new_path)
            map[node[1]][node[0]] = '.'

    # paint the tiles
    for tile in tiles:
        map[tile[1]][tile[0]] = 'O'

    return len(tiles)

if __name__ == '__main__':

    file = './16/input.txt'

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