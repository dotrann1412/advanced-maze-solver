from algorithms.algorithms_utils import *
from utils import manhattan_distance, euclidean_distance
from constants import *
from queue import PriorityQueue

'''
    A* algorithm for normal maze
    Heuristic function: Manhattan distance between current point and end point

    Args:
        graph: 2D array of graph
        start: starting point
        end: ending point
        callback: function to visualize the algorithm
        hf: heuristic function

    Returns:
        list of points from start to end
'''
def __normalAStar(graph, start, end, callback, hf):
    def h(point):
        return hf(point, end)

    dim = [len(graph), len(graph[0])]
    sleep_time = calcSleepTime(dim)

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
            if not isInGraph(graph, child) or graph[child[0]][child[1]] != MazeObject.EMPTY:
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

def __aStarWithBonusPoint(graph, start, end, bonus_points, callback, hf):
    pass

def __aStarIntermediatePoint(graph, start, end, intermediate_points, callback, hf):
    pass

def __aStarWithTeleportPoint(graph, start, end, teleport_points, callback, hf):
    pass


def aStar(graph, start, end, mode, bonus_points, intermediate_points, teleport_points, callback, hf=manhattan_distance):
    if not isValidGraph(graph):
        return None

    if mode == AlgorithmsMode.NORMAL:
        return __normalAStar(graph, start, end, callback, hf)

    if mode == AlgorithmsMode.BONUS_POINT:
        return __aStarWithBonusPoint(graph, start, end, bonus_points, callback, hf)

    if mode == AlgorithmsMode.INTERMEDIATE_POINT:
        return __aStarIntermediatePoint(graph, start, end, intermediate_points, callback, hf)

    if mode == AlgorithmsMode.TELEPORT_POINT:
        return __aStarWithTeleportPoint(graph, start, end, teleport_points, callback, hf)
