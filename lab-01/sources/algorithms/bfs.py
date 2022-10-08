from algorithms.algorithms_utils import *
from .. import constants
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

			if isExit(graph[next_step_x][next_step_y]):
				parrent[next_step_x][next_step_y] = current
				found = True
				break

			if isEmptyCell(graph[next_step_x][next_step_y]) and not parrent[next_step_x][next_step_y]:
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

def __bfs_with_bonus_point(graph, starting_point, ending_point, bonus_point_list, callback):
	size = grapthSize(graph)

def __bfs_intermediate_point(graph, starting_point, ending_point, itermediate_point_list, callback):
	size = grapthSize(graph)

def __bfs_with_teleport_point(graph, starting_point, ending_point, teleport_list, callback):
	size = grapthSize(graph)
	frontier = []

	ignore_teleport = False

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

			if isExit(graph[next_step_x][next_step_y]):
				parrent[next_step_x][next_step_y] = current
				found = True
				break

			if not ignore_teleport and isTeleportCell(graph[next_step_x][next_step_y]):
				for teleport in teleport_list:
					parrent[teleport[0]][teleport[1]] = current if teleport == [next_step_x, next_step_y] else [next_step_x, next_step_y]
					frontier.append(teleport)
				ignore_teleport = True

			if isEmptyCell(graph[next_step_x][next_step_y]) and not parrent[next_step_x][next_step_y]:
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


def bfs(graph, starting_point, ending_point, mode, call_back,
	teleport_list = [], bonus_point_list = [], itermediate_point_list = []):
	
	if not isValidGraph(graph):
		return None

	if mode == AlgorithmsMode.NORMAL:
		return __normal_bfs(graph, call_back)

	if mode == AlgorithmsMode.BONUS_POINT:
		return __bfs_with_bonus_point(graph, starting_point, ending_point, bonus_point_list, call_back)

	if mode == AlgorithmsMode.INTERMEDIATE_POINT:
		return __bfs_intermediate_point(graph, starting_point, ending_point, itermediate_point_list, call_back)

	if mode == AlgorithmsMode.TELEPORT_POINT:
		return __bfs_with_teleport_point(graph, starting_point, ending_point, call_back)
