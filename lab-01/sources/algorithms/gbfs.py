from numpy import empty
from algorithms.algorithms_utils import *
from constants import *
from utils import euclidean_distance, manhattan_distance

class PriorityQueue(object):
    '''
    type must be in ['big', 'small']
    '''
    def __init__(self, heuristic, goal, type='big'):
        assert(len(goal) == 2)
        assert(heuristic(goal, goal) == 0)
        assert(type in ['big', 'small'])
        self.queue = []
        self.heuristic = heuristic
        self.goal = goal
        self.type = type

    def __str__(self) -> str:
        return ' '.join([str(element) for element in self.queue]) if not self.empty() else 'empty'

    def size(self) -> int:
        return len(self.queue)

    def empty(self):
        return self.size() <= 0

    def push(self, element):
        self.queue.append(element)

    def pop(self):
        try:
            arg = 0
            for i in range(1, len(self.queue)):
                if self.compare()(self.heuristic(self.queue[i], self.goal), self.heuristic(self.queue[arg], self.goal)):
                    arg = i
            item = self.queue[arg]
            del self.queue[arg]
            return item
        except:
            print('Priority queue is empty!')
            return None

    def compare(self):
        if self.type == 'big':
            return lambda a, b: a > b
        else:  # small
            return lambda a, b: a < b

'''
    Args:
        graph: 2D array of graph
        start: starting point
        end: ending point
        callback: function to visualize the algorithm
        hf: heuristic function

    Returns:
        list of points from start to end
'''
def __normalGbfs(graph, start, end, callback, hf):
    terminated = [-1, -1]
    dim = [len(graph), len(graph[0])]

    priority_queue = PriorityQueue(heuristic=hf, goal=end, type='small')

    if start[0] < 0 or start[0] >= dim[0] or start[1] < 0 or start[1] >= dim[1]:
        print("[DEBUG] Invalid starting point...")
        return None

    parent = [[None for __ in range(dim[1])] for _ in range(dim[0])]

    priority_queue.push(start)
    parent[start[0]][start[1]] = terminated

    found = False

    while priority_queue.size() != 0 and not found:
        current = priority_queue.pop()
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
                priority_queue.push(next_step)
        
        if current != start:
            callback(current[1], current[0], Colors.FRONTIER_COLOR, sleep_time=30)

    if not end or not parent[end[0]][end[1]]:
        print("[DEBUG] Unreachable...")
        return None
    
    answer = []
    pointer = end

    while parent[pointer[0]][pointer[1]] != terminated:
        answer.append(pointer)
        pointer = parent[pointer[0]][pointer[1]]

    for point in answer[1:]:
        callback(point[1], point[0], Colors.PATH_COLOR, sleep_time=10)

    return answer[::-1]

def __gbfsWithBonusPoint(graph, start, end, bonus_points, callback, hf):
    pass

def __gbfsIntermediatePoint(graph, start, end, intermediate_points, callback, hf):
    pass

def __gbfsWithTeleportPoint(graph, start, end, teleport_points, callback, hf):
    pass

def gbfs(graph, start, end, mode, bonus_points, intermediate_points, teleport_points, callback, hf=manhattan_distance):
    if not isValidGraph(graph):
        return None

    if mode == AlgorithmsMode.NORMAL:
        return __normalGbfs(graph, start, end, callback, hf)

    if mode == AlgorithmsMode.BONUS_POINT:
        return __gbfsWithBonusPoint(graph, start, end, bonus_points, callback, hf)

    if mode == AlgorithmsMode.INTERMEDIATE_POINT:
        return __gbfsIntermediatePoint(graph, start, end, intermediate_points, callback, hf)

    if mode == AlgorithmsMode.TELEPORT_POINT:
        return __gbfsWithTeleportPoint(graph, start, end, teleport_points, callback, hf)

