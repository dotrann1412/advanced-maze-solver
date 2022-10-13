from algorithms.algorithms_utils import *
from constants import *

def __normal_bfs(graph, starting_point, ending_point, callback):
	size = [len(graph), len(graph[0])]
	frontier = []

	if starting_point[0] < 0 or starting_point[0] >= size[0] or starting_point[1] < 0 or starting_point[1] >= size[1]:
		return None

	parrent = [[None for __ in range(size[1])] for _ in range(size[0])]
	
	frontier.append(starting_point)
	parrent[starting_point[0]][starting_point[1]] = starting_point
	
	found = False

	while len(frontier) != 0 and not found:
		current = frontier[0]
		frontier.pop(0)

		if current != starting_point:
			callback(current[1], current[0], Colors.FRONTIER_COLOR)

		for element in direction:
			next_step_x, next_step_y = current[0] + element[0], current[1] + element[1]
			
			if next_step_x < 0 or next_step_x >= size[0] or next_step_y < 0 or next_step_y >= size[1]:
				continue

			if (next_step_x, next_step_y) == ending_point:
				parrent[next_step_x][next_step_y] = current
				found = True
				break

			if graph[next_step_x][next_step_y] == MazeObject.EMPTY and not parrent[next_step_x][next_step_y]:
				parrent[next_step_x][next_step_y] = current
				frontier.append([next_step_x, next_step_y])

	if not ending_point or not parrent[ending_point[0]][ending_point[1]]:
		return None

	answer = []
	pointer = ending_point

	limit = size[0] + size[1]

	while pointer != starting_point:
		answer.append(pointer)
		pointer = parrent[pointer[0]][pointer[1]]

		limit -= 1
		if limit == 0:
			raise Exception("Infinite loop!")

	answer.append(starting_point)
	answer = answer[::-1]

	for point in answer:
		callback(point[1], point[0], Colors.PATH_COLOR)

	return answer

def __bfs_with_bonus_point(graph, starting_point, ending_point, bonus_points, callback):
	size = grapthSize(graph)

def __bfs_intermediate_point(graph, starting_point, ending_point, intermediate_points, callback):
	size = grapthSize(graph)

def __bfs_with_teleport_point(graph, starting_point, ending_point, teleport_points, callback):
	size = [len(graph), len(graph[0])]
	frontier = []

	if starting_point[0] < 0 or starting_point[0] >= size[0] or starting_point[1] < 0 or starting_point[1] >= size[1]:
		return None

	parrent = [[None for __ in range(size[1])] for _ in range(size[0])]
	
	frontier.append(starting_point)
	parrent[starting_point[0]][starting_point[1]] = starting_point
	
	found = False

	while len(frontier) != 0 and not found:
		current = frontier[0]
		frontier.pop(0)

		if current != starting_point:
			callback(current[1], current[0], Colors.FRONTIER_COLOR)

		for element in direction:
			next_x, next_y = current[0] + element[0], current[1] + element[1]
			
			if isInGraph(graph, (next_x, next_y)) or graph[next_x][next_y] == MazeObject.EMPTY:
				continue

			if graph[next_x][next_y] == ending_point:
				parrent[next_x][next_y] = current
				found = True
				break

			if (next_x, next_y) in teleport_points:
				destination_x, destination_y = teleport_points[(next_x, next_y)]

				if graph[destination_x][destination_y] == ending_point:
					parrent[destination_x][destination_y] = current
					found = True
					break

				if not parrent[destination_x][destination_y]:
					parrent[destination_x][destination_y] = current
					frontier.append([destination_x, destination_y])

			if  not parrent[next_x][next_y]:
				parrent[next_x][next_y] = current
				frontier.append([next_x, next_y])

	if not ending_point or not parrent[ending_point[0]][ending_point[1]]:
		return None

	answer = []
	pointer = ending_point

	limit = size[0] + size[1]

	while pointer != starting_point:
		answer.append(pointer)
		pointer = parrent[pointer[0]][pointer[1]]

		limit -= 1
		if limit == 0:
			raise Exception("Infinite loop!")

	answer.append(starting_point)
	answer = answer[::-1]

	for point in answer:
		callback(point[1], point[0], Colors.PATH_COLOR)

	return answer


def bfs(graph, starting_point, ending_point, mode, bonus_points, intermediate_points, teleport_points, call_back, hf=None):
	
	if not isValidGraph(graph):
		return None

	if mode == AlgorithmsMode.NORMAL:
		return __normal_bfs(graph, call_back)

	if mode == AlgorithmsMode.BONUS_POINT:
		return __bfs_with_bonus_point(graph, starting_point, ending_point, bonus_points, call_back)

	if mode == AlgorithmsMode.INTERMEDIATE_POINT:
		return __bfs_intermediate_point(graph, starting_point, ending_point, intermediate_points, call_back)

	if mode == AlgorithmsMode.TELEPORT_POINT:
		return __bfs_with_teleport_point(graph, starting_point, ending_point, teleport_points, call_back)
