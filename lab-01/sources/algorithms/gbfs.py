from algorithms.algorithms_utils import *
from constants import *
from utils import manhattan_distance
from queue import PriorityQueue
from visualizer import set_path_color, set_frontier_color


def __normalGbfs(graph, start, end, hf):
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
        _h, current = priority_queue.get()

        if current != start and current:
            set_frontier_color(current[1], current[0], sleep_time // 10)

        for element in direction:
            next_step_x, next_step_y = current[0] + element[0], current[1] + element[1]

            if not isInGraph(graph, (next_step_x, next_step_y)) or graph[next_step_x][next_step_y] == MazeObject.WALL or parent[next_step_x][next_step_y]:
                continue

            if (next_step_x, next_step_y)  == end:
                parent[end[0]][end[1]] = current
                found = True
                break
            
            parent[next_step_x][next_step_y] = current
            priority_queue.put((h((next_step_x, next_step_y)) ,(next_step_x, next_step_y )))

    if not end or not parent[end[0]][end[1]]:
        return None

    answer = []
    pointer = end

    while parent[pointer[0]][pointer[1]] != terminated:
        answer.append(pointer)
        pointer = parent[pointer[0]][pointer[1]]
    answer.append(start)
    
    answer = answer[::-1]

    set_path_color(answer, sleep_time, [start, end])

    return answer

def __gbfsWithBonusPoint(graph, start, end, bonus_points, hf):
    pass

def __gbfsIntermediatePoint(graph, start, end, intermediate_points, hf):
    pass

def __gbfsWithTeleportPoint(graph, start, end, teleport_points: dict, heuristic):
    terminated = [-1, -1]
    size = grapthSize(graph)
    sleep_time = calcSleepTime(size)

    priority_queue = PriorityQueue()
    special_points = [end] + list(teleport_points.keys())

    def __extra_heuristic(point):
        val = INF
        for p in special_points:
            val = min(val, heuristic(p, end) + heuristic(point, p))
            if p in teleport_points:
                val = min(val, heuristic(teleport_points[p], end), heuristic(point, p))
        return val

    if not isInGraph(graph, start):
        print("[DEBUG] Invalid starting point...")
        return None

    parent = [[None for __ in range(size[1])] for _ in range(size[0])]

    priority_queue.put((__extra_heuristic(start), start))
    parent[start[0]][start[1]] = terminated

    found = False
    while not priority_queue.empty() and not found:
        hf, current = priority_queue.get()
        
        if current != start and current not in teleport_points:
            set_frontier_color(current[1], current[0], sleep_time)
        
        for d in direction:
            next_x, next_y = current[0] + d[0], current[1] + d[1]

            if not isInGraph(graph, (next_x, next_y)) or graph[next_x][next_y] == MazeObject.WALL or parent[next_x][next_y]:
                continue
        
            if (next_x, next_y) == end:
                parent[end[0]][end[1]] = current
                found = True
                break

            if (next_x, next_y) in teleport_points:
                destination_x, destination_y = teleport_points[(next_x, next_y)]
                if not parent[destination_x][destination_y]:
                    parent[destination_x][destination_y] = current
                    priority_queue.put((__extra_heuristic((destination_x, destination_y)), (destination_x, destination_y)))
            
            parent[next_x][next_y] = current
            priority_queue.put((__extra_heuristic((next_x, next_y)) , (next_x, next_y)))

    if not end or not parent[end[0]][end[1]]:
        print("[DEBUG] Unreachable...")
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

