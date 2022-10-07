from algorithms.algorithms_utils import *
from constants import *

def __detect_starting_point(graph):
	pass

def __normal_bfs(graph):
	dim = [len(graph), len(graph[0])]
	queue = []
	starting_point = __detect_starting_point(graph)
	# parrent = [[for __ in range(dim[1])] for _ in (dim[0])]
	queue.append(starting_point)

def __bfs_with_bonus_point(graph):
	starting_point = __detect_starting_point(graph)

def __bfs_intermediate_point(graph):
	starting_point = __detect_starting_point(graph)

def __bfs_with_teleport_point(graph):
	starting_point = __detect_starting_point(graph)

def bfs(graph, mode):
	if not valid_graph(graph):
		return None

	if mode == AlgorithmsMode.NORMAL:
		return __normal_bfs(graph)

	if mode == AlgorithmsMode.BONUS_POINT:
		return __bfs_with_bonus_point(graph)
	
	if mode == AlgorithmsMode.INTERMEDIATE_POINT:
		return __bfs_intermediate_point(graph)
	
	if mode == AlgorithmsMode.TELEPORT_POINT:
		return __bfs_with_teleport_point(graph)


'''
BFS for visualization testing
    `callback` has 4 parameters: (x, y, color, slee_time=30)
'''
def bfs_testing(matrix, start, end, callback):
    # use terminated to stop the algorithm
    # (this will be starting points's parent)
    terminated = (-1, -1)

    dim = [len(matrix), len(matrix[0])]
    sleep_time = calc_sleep_time(dim)
    queue = []

    if start[0] < 0 or start[0] >= dim[0] or start[1] < 0 or start[1] >= dim[1]:
        return None

    parent = [[None for __ in range(dim[1])] for _ in range(dim[0])]

    queue.append(start)
    parent[start[0]][start[1]] = terminated

    found = False

    while len(queue) != 0 and not found:
        current = queue[0]
        queue.pop(0)
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
                queue.append(next_step)

        # set color at current point. notice that we do not change the color of starting and ending point
        if current != start:
            callback(current[1], current[0], FRONTIER_COLOR, sleep_time)

    if not end or not parent[end[0]][end[1]]:
        return None

    answer = []
    pointer = end

    while parent[pointer[0]][pointer[1]] != terminated:
        answer.append(pointer)
        pointer = parent[pointer[0]][pointer[1]]

    # set color for points in answer (optimize path)
    for point in answer[1:]:
        callback(point[1], point[0], PATH_COLOR, sleep_time)

    return answer[::-1]

