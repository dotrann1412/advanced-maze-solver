from algorithms.algorithms_utils import *
from constants import *
from queue import PriorityQueue

'''
    A* algorithm for normal maze
    Heuristic function: Manhattan distance between current point and end point

    I have also added an option to use Euclidean distance as heuristic function
'''
def __normalAStar(matrix, start, end, callback, euclid = False):
    def h(point):
        if euclid:
            return ((point[0] - end[0]) ** 2 + (point[1] - end[1]) ** 2) ** 0.5
        return abs(point[0] - end[0]) + abs(point[1] - end[1])

    dim = [len(matrix), len(matrix[0])]
    sleep_time = calcSleepTime(dim)
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
            callback(point[1], point[0], Colors.FRONTIER_COLOR, sleep_time)

        for d in direction:
            child = (point[0] + d[0], point[1] + d[1])
            if not isInGraph(matrix, child) or matrix[child[0]][child[1]] != Colors.EMPTY:
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
        callback(point[1], point[0], Colors.PATH_COLOR, sleep_time)
    
    return answer

def __aStarWithBonusPoint(graph):
    pass

def __aStarIntermediatePoint(graph):
    pass

def __aStarWithTeleportPoint(graph):
    pass


def aStar(graph, start, end, mode, callback, *args):
    if not isValidGraph(graph):
        return None

    if mode == AlgorithmsMode.NORMAL:
        return __normalAStar(graph, start, end, callback, *args)

    if mode == AlgorithmsMode.BONUS_POINT:
        return __aStarWithBonusPoint(graph)

    if mode == AlgorithmsMode.INTERMEDIATE_POINT:
        return __aStarIntermediatePoint(graph)

    if mode == AlgorithmsMode.TELEPORT_POINT:
        return __aStarWithTeleportPoint(graph)
