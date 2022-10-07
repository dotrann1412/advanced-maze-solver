from algorithms.algorithms_utils import *
from constants import *
from queue import PriorityQueue

'''
    A* algorithm for normal maze
    Heuristic function: Manhattan distance between current point and end point

    I have also added an option to use Euclidean distance as heuristic function
'''
def __normal_a_star(matrix, start, end, callback, euclid = False):
    def h(point):
        if euclid:
            return ((point[0] - end[0]) ** 2 + (point[1] - end[1]) ** 2) ** 0.5
        return abs(point[0] - end[0]) + abs(point[1] - end[1])

    dim = [len(matrix), len(matrix[0])]
    sleep_time = calc_sleep_time(dim)
    print('Sleep time:', sleep_time)

    parent = [[None for __ in range(dim[1])] for _ in range(dim[0])]
    g = [[float('inf') for __ in range(dim[1])] for _ in range(dim[0])]
    g[start[0]][start[1]] = 0

    pq = PriorityQueue()
    # pq compare f, then h (if f of two node are equal)
    pq.put([g[start[0]][start[1]] + h(start), h(start), start])

    found = False
    while not pq.empty():
        _, _, point = pq.get()

        if point == end:
            found = True
            break
            
        if point != start:
            callback(point[1], point[0], FRONTIER_COLOR, sleep_time)

        for d in direction:
            child = (point[0] + d[0], point[1] + d[1])
            if not is_in_graph(matrix, child) or matrix[child[0]][child[1]] != EMPTY:
                continue

            if g[child[0]][child[1]] > g[point[0]][point[1]] + 1:
                g[child[0]][child[1]] = g[point[0]][point[1]] + 1
                parent[child[0]][child[1]] = point
                pq.put([g[child[0]][child[1]] + h(child), h(child), child])
        
    if not found:
        return None
    
    answer = []
    pointer = end

    while pointer != start:
        answer.append(pointer)
        pointer = parent[pointer[0]][pointer[1]]
    answer.append(start)

    for point in answer[1:-1]:
        callback(point[1], point[0], PATH_COLOR, sleep_time)
    
    return answer

def __a_star_with_bonus_point(graph):
    pass

def __a_star_intermediate_point(graph):
    pass

def __a_star_with_teleport_point(graph):
    pass


def a_star(graph, start, end, mode, callback, *args):
    if not valid_graph(graph):
        return None

    if mode == AlgorithmsMode.NORMAL:
        return __normal_a_star(graph, start, end, callback, *args)

    if mode == AlgorithmsMode.BONUS_POINT:
        return __a_star_with_bonus_point(graph)

    if mode == AlgorithmsMode.INTERMEDIATE_POINT:
        return __a_star_intermediate_point(graph)

    if mode == AlgorithmsMode.TELEPORT_POINT:
        return __a_star_with_teleport_point(graph)
