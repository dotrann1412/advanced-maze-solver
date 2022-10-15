from algorithms.algorithms_utils import *
from constants import *
from utils import manhattan_distance
from queue import PriorityQueue
from visualizer import set_path_color, set_frontier_color

def __normalGbfs(graph, start, end, heuristic):
    def h(point):
        return heuristic(point, end)

    terminated = [-1, -1]
    dim = [len(graph), len(graph[0])]
    sleep_time = calcSleepTime(dim)

    priority_queue = PriorityQueue()

    if start[0] < 0 or start[0] >= dim[0] or start[1] < 0 or start[1] >= dim[1]:
        return None

    parent = [[None for __ in range(dim[1])] for _ in range(dim[0])]

    priority_queue.put([h(start), start])
    parent[start[0]][start[1]] = terminated

    found = False

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
            
            if (graph[next_step[0]][next_step[1]] == ' ') and not parent[next_step[0]][next_step[1]]:
                parent[next_step[0]][next_step[1]] = current
                priority_queue.put([h(next_step), next_step])
        
        if current != start:
            set_frontier_color(current[1], current[0], sleep_time)

    if not end or not parent[end[0]][end[1]]:
        return None
    
    answer = []
    pointer = end

    while parent[pointer[0]][pointer[1]] != terminated:
        answer.append(pointer)
        pointer = parent[pointer[0]][pointer[1]]
    answer.append(start)
    
    answer = answer[::-1]

    set_path_color(answer, sleep_time)

    return answer

def __gbfsWithBonusPoint(graph, start, end, bonus_points, hf):
    pass

def __gbfsIntermediatePoint(graph, start, end, intermediate_points, hf):
    pass

def __gbfsWithTeleportPoint(graph, start, end, teleport_points, hf):
    pass

def gbfs(graph, start, end, mode, bonus_points, intermediate_points, teleport_points, hf=manhattan_distance):
    if not isValidGraph(graph):
        return None

    if mode == AlgorithmsMode.NORMAL:
        return __normalGbfs(graph, start, end, hf)

    if mode == AlgorithmsMode.BONUS_POINT:
        return __gbfsWithBonusPoint(graph, start, end, bonus_points, hf)

    if mode == AlgorithmsMode.INTERMEDIATE_POINT:
        return __gbfsIntermediatePoint(graph, start, end, intermediate_points, hf)

    if mode == AlgorithmsMode.TELEPORT_POINT:
        return __gbfsWithTeleportPoint(graph, start, end, teleport_points, hf)

