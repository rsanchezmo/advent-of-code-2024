import time
from dataclasses import dataclass
import heapq
from pprint import pprint

def parse_input(file: str) -> list:
    with open(file, 'r') as f:
        lines = f.readlines()

    bytes_ = []
    for line in lines:
        line = line.strip()
        bytes_.append(list(map(int, line.split(','))))
    return bytes_

MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Down, Up, Right, Left

@dataclass
class Node:
    pos: tuple
    cost: int
    parent: 'Node' = None

    def __lt__(self, other):
        return self.cost < other.cost
    
def heuristic(node: Node, goal: Node) -> int:
    return abs(node.pos[0] - goal.pos[0]) + abs(node.pos[1] - goal.pos[1])
    
def a_star(map_, orig, goal):
    orig_node = Node(pos=orig, cost=0)
    goal_node = Node(pos=goal, cost=0)

    # Priority queue for open list
    open_list = []
    heapq.heappush(open_list, (heuristic(orig_node, goal_node), orig_node))

    visited_cost = {}  # Tracks minimum cost at which each node was visited

    while open_list:
        _, current_node = heapq.heappop(open_list)

        # Goal check
        if current_node.pos == goal_node.pos:
            cost = current_node.cost
            path = []
            while current_node:
                path.append(current_node.pos)
                current_node = current_node.parent
            return path[::-1], cost

        # Add to visited with its cost
        if current_node.pos in visited_cost and visited_cost[current_node.pos] <= current_node.cost:
            continue
        visited_cost[current_node.pos] = current_node.cost

        # Explore neighbors
        for delta_x, delta_y in MOVES:
            new_x = current_node.pos[0] + delta_x
            new_y = current_node.pos[1] + delta_y

            # Check bounds and obstacles
            if new_x < 0 or new_x >= len(map_[0]) or new_y < 0 or new_y >= len(map_) or map_[new_y][new_x] == '#':
                continue

            new_cost = current_node.cost + 1  # Assuming uniform cost for moves
            new_node = Node(pos=(new_x, new_y), cost=new_cost, parent=current_node)

            # Skip if already visited with a lower or equal cost
            if new_node.pos in visited_cost and visited_cost[new_node.pos] <= new_cost:
                continue

            priority = new_cost + heuristic(new_node, goal_node)
            heapq.heappush(open_list, (priority, new_node))

    return [], float('inf')  # No path found

def part_a(file: str)  -> int:
    bytes_ = parse_input(file)

    orig = (0, 0)
    goal = (70, 70)

    map = [['.' for _ in range(goal[1]+1)] for _ in range(goal[0]+1)]
    
    for i in range(1024):
        if i >= len(bytes_):
            break
        col, row = bytes_[i]
        map[row][col] = '#'
    
    # now a-star
    path, _ = a_star(map, orig, goal)

    return len(path)-1

def part_b(file: str)  -> int:
    bytes_ = parse_input(file)

    orig = (70, 70)
    goal = (0, 0)

    map = [['.' for _ in range(71)] for _ in range(71)]
    
    for i in range(1024):
        col, row = bytes_[i]
        map[row][col] = '#'
    
    # now a-star
    path = True
    idx = 1024
    while path:
        map[bytes_[idx][1]][bytes_[idx][0]] = '#'
        path, _ = a_star(map, orig, goal)
        idx += 1

    return bytes_[idx-1]

if __name__ == '__main__':

    file = './18/input.txt'

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