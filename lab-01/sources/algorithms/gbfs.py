from numpy import empty
from algorithms.algorithms_utils import direction, valid_graph, AlgorithmsMode
from constants import *
from utils import euclidean_distance, manhattan_distance
from queue import PriorityQueue


def gbfs(matrix, start, end, callback, heuristic):
    def h(point):
        return heuristic(point, end)

    terminated = [-1, -1]
    dim = [len(matrix), len(matrix[0])]

    priority_queue = PriorityQueue()
    print("[DEBUG] Priority queue created...")

    if start[0] < 0 or start[0] >= dim[0] or start[1] < 0 or start[1] >= dim[1]:
        print("[DEBUG] Invalid starting point...")
        return None

    print("[DEBUG] Starting point checked...")

    parent = [[None for __ in range(dim[1])] for _ in range(dim[0])]

    priority_queue.put([h(start), start])
    parent[start[0]][start[1]] = terminated

    found = False

    print("[DEBUG] Go into loop...")

    while not priority_queue.empty() and not found:
        _, current = priority_queue.get()
        if current == end:
            pass
        
        for element in direction:
            next_step = current[0] + element[0], current[1] + element[1]

            if next_step[0] < 0 or next_step[0] >= dim[0] or next_step[1] < 0 or next_step[1] >= dim[1]:
                continue
        
            if next_step == end:
                parent[end[0]][end[1]] = current
                found = True
                break
            
            if (matrix[next_step[0]][next_step[1]] == ' ') and not parent[next_step[0]][next_step[1]]:
                parent[next_step[0]][next_step[1]] = current
                priority_queue.put([h(next_step), next_step])
        
        if current != start:
            callback(current[1], current[0], FRONTIER_COLOR, sleep_time=30)

    if not end or not parent[end[0]][end[1]]:
        print("[DEBUG] Unreachable...")
        return None
    
    answer = []
    pointer = end

    print("[DEBUG] Tracing back the path...")
    while parent[pointer[0]][pointer[1]] != terminated:
        answer.append(pointer)
        pointer = parent[pointer[0]][pointer[1]]

    for point in answer[1:]:
        callback(point[1], point[0], PATH_COLOR, sleep_time=10)

    return answer[::-1]



