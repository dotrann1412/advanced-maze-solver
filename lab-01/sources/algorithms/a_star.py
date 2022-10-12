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
        drawPath: draw path or not (default True, we use this for other map)

    Returns:
        list of points from start to end
'''
def __normalAStar(graph, start, end, callback, hf, drawPath=True):
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
            if not isInGraph(graph, child) or graph[child[0]][child[1]] == MazeObject.WALL:
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

    if drawPath:
        for point in answer[1:-1]:
            callback(point[1], point[0], Colors.PATH_COLOR, sleep_time)
        
    return answer


def __aStarWithBonusPointRecur(graph, start, end, bonus_points, callback, hf):
    def h(p1, p2=end):
        return hf(p1, p2)

    def calcHBonus(start, bonus, end):
        return h(start, bonus[:2]) + +  h(bonus[:2], end) + bonus[2]

    hBonusArr = sorted([[calcHBonus(start, bonus, end), bonus] for bonus in bonus_points])
    hStart = h(start)

    for hBonusItem in hBonusArr:
        hBonus, bonus = hBonusItem
        
        if hBonus >= hStart:
            break

        part1 = __normalAStar(graph, start, bonus[:2], callback, hf, drawPath=False)
        if part1 is None:
            continue
        next_bonus_points = bonus_points.copy()
        next_bonus_points.remove(bonus)
        part2 = __aStarWithBonusPointRecur(graph, bonus[:2], end, next_bonus_points, callback, hf)
        if part2 is None:
            continue
        return part2 + part1
    
    return __normalAStar(graph, start, end, callback, hf, drawPath=False)

def __aStarWithBonusPoint(graph, start, end, bonus_points, callback, hf):
    dim = [len(graph), len(graph[0])]
    sleep_time = calcSleepTime(dim)

    answer = __aStarWithBonusPointRecur(graph, start, end, bonus_points, callback, hf)

    bonus_dict = {}
    for bonus in bonus_points:
        bonus_dict[bonus[:2]] = [bonus[2], False]   # bonus point, is visited
    
    cost = len(answer) - 1
    for point in answer:
        if point in bonus_dict:
            cost += bonus_dict[point][0]
            bonus_dict[point][0] = 0
            bonus_dict[point][1] = True    

    # reset color of start and end
    callback(start[1], start[0], color=Colors.START_COLOR, sleep_time=0)
    callback(end[1], end[0], color=Colors.END_COLOR, sleep_time=0)

    # draw un-passed bonus
    for bonus in bonus_dict:
        if bonus_dict[bonus][1] == False:
            callback(bonus[1], bonus[0], Colors.BONUS_COLOR, 0)
            
    # draw path
    for point in answer[1:-1]:
        color = Colors.PATH_COLOR if point not in bonus_dict else Colors.BONUS_PASSED
        callback(point[1], point[0], color, sleep_time)
    
        
    return answer, cost
        

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
