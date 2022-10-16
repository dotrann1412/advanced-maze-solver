from algorithms.algorithms_utils import *
from constants import *
from utils import manhattan_distance
from queue import PriorityQueue
from visualizer import set_path_color, set_frontier_color


def __normalGbfs(graph, start, end, heuristic):
    def h(point):
        return hf(point, end)
    terminated = [-1, -1]
    dim = grapthSize(graph)
    sleep_time = calcSleepTime(dim)

    priority_queue = PriorityQueue()

    if not isInGraph(graph, start):
        print("[DEBUG] Invalid starting point...")
        return None

    parent = [[None for __ in range(dim[1])] for _ in range(dim[0])]

    priority_queue.put((h(start), start))
    parent[start[0]][start[1]] = terminated

    found = False
    
    while not priority_queue.empty() and not found:
        _h, current_pos = priority_queue.get()
        
        for element in direction:
            next_step_x, next_step_y = current_pos[0] + element[0], current_pos[1] + element[1]

            if not isInGraph(graph, (next_step_x, next_step_y)) or graph[next_step_x][next_step_y] == MazeObject.WALL or parent[next_step_x][next_step_y]:
                continue
        
            if (next_step_x, next_step_y)  == end:
                parent[end[0]][end[1]] = current_pos
                found = True
                break
            
            parent[next_step_x][next_step_y] = current_pos
            priority_queue.put((h((next_step_x, next_step_y)) ,(next_step_x, next_step_y )))
        
        if current_pos != start:
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

    for point in answer[1:]:
        set_path_color(answer, sleep_time)

    return answer

def __gbfsWithBonusPoint(graph, start, end, bonus_points, hf):
    pass

def __gbfsIntermediatePoint(graph, start, end, intermediate_points, hf):
    pass

def __gbfsWithTeleportPoint(graph, start, end, teleport_points, hf):
    terminated = [-1, -1]
    size = grapthSize(graph)

    priority_queue = PriorityQueue()

    if not isInGraph(graph, start):
        print("[DEBUG] Invalid starting point...")
        return None

    parent = [[None for __ in range(size[1])] for _ in range(size[0])]

    priority_queue.put((hf(start, end), start))
    parent[start[0]][start[1]] = terminated

    found = False
    while not priority_queue.empty() and not found:
        hf_value, current_pos = priority_queue.get()
        
        if current_pos != start and current_pos not in teleport_points:
          set_frontier_color(current_pos[1], current_pos[0], sleep_time)
        
        for element in direction:
            next_step_x, next_step_y = current_pos[0] + element[0], current_pos[1] + element[1]

            if not isInGraph(graph, (next_step_x, next_step_y)) or graph[next_step_x][next_step_y] == MazeObject.WALL or parent[next_step_x][next_step_y]:
                continue
        
            if (next_step_x, next_step_y)  == end:
                parent[end[0]][end[1]] = current_pos
                found = True
                break

            if (next_step_x, next_step_y) in teleport_points:
                destination_x, destination_y = teleport_points[(next_step_x, next_step_y)]
                if not parent[destination_x][destination_y]:
                    parent[destination_x][destination_y] = current_pos
                    priority_queue.put((hf((destination_x, destination_y), end) ,(destination_x, destination_y )))
            
            parent[next_step_x][next_step_y] = current_pos
            priority_queue.put((hf((next_step_x, next_step_y), end) ,(next_step_x, next_step_y )))
        
        if current_pos != start:
            callback(current_pos[1], current_pos[0], Colors.FRONTIER_COLOR, sleep_time=0)

    if not end or not parent[end[0]][end[1]]:
        print("[DEBUG] Unreachable...")
        return None
    
    answer = []
    pointer = end

    while parent[pointer[0]][pointer[1]] != terminated:
        answer.append(pointer)
        pointer = parent[pointer[0]][pointer[1]]

    for point in answer[1:-1]:
        set_path_color(answer, sleep_time)

    return answer[::-1]

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

