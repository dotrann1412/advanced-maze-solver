from algorithms_utils import *
from queue import PriorityQueue

def __normal_ucs(graph, starting_point, ending_point, callback):
	frontier = PriorityQueue
	size = grapthSize(graph)
	
	parrent = [[None for __ in size[1]] for _ in size[0]]
	cost = [[INF for __ in size[1]] for _ in size[0]]

	frontier.put([0, starting_point])
	cost[starting_point[0]][starting_point[1]] = 0
	parrent[starting_point[0]][starting_point[1]] = starting_point

	found = False
	while not frontier.empty() and not found:
		current_cost, current_point = frontier.get()

		if cost[current_point[0]][current_point[1]] != current_cost:
			continue
		
		for dir in direction:
			next_x, next_y = current_point[0] + dir[0], current_point[1] + dir[1]
			
			if next_x < 0 or next_x >= size[0] or next_y < 0 or next_y >= size[1]:
				continue
			
			if cost[next_x][next_y] > current_cost + 1:
				cost[next_x][next_y] = current_cost + 1
				parrent[next_x][next_y] = current_point
				
				if [next_x, next_y] == ending_point:
					found = True
					break

				frontier.put(cost[next_x][next_y] ,[next_x, next_y])

	if not found:
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
	return answer

def __ucs_with_bonus_point(graph, starting_point, ending_point, bonus_point_list, callback):
	pass

def __ucs_intermediate_point(graph, starting_point, ending_point, itermediate_point_list, callback):
	pass

def __ucs_with_teleport_point(graph, starting_point, ending_point, teleport_list, callback):
	frontier = PriorityQueue
	size = grapthSize(graph)
	
	parrent = [[None for __ in size[1]] for _ in size[0]]
	cost = [[INF for __ in size[1]] for _ in size[0]]

	frontier.put([0, starting_point])
	cost[starting_point[0]][starting_point[1]] = 0
	parrent[starting_point[0]][starting_point[1]] = starting_point

	found = False
	while not frontier.empty() and not found:
		current_cost, current_point = frontier.get()

		if cost[current_point[0]][current_point[1]] != current_cost:
			continue

		if current_point != starting_point:
			callback(current_point[1], current_point[0], FRONTIER_COLOR)
		
		for dir in direction:
			next_x, next_y = current_point[0] + dir[0], current_point[1] + dir[1]
			
			if next_x < 0 or next_x >= size[0] or next_y < 0 or next_y >= size[1] or not isEmptyCell(graph[next_x][next_y]):
				continue

			if [next_x, next_y] in teleport_list and not found:
				for teleport in teleport_list:
					if cost[teleport[0]][teleport[1]] > current_cost + 1:
						cost[teleport[0]][teleport[1]] = current_cost + 1
						parrent[teleport[0]][teleport[1]] = current_point

					# case not occur
					if [next_x, next_y] == ending_point:
						found = True
						break

					frontier.put(cost[next_x][next_y], [next_x, next_y])
			
			if cost[next_x][next_y] > current_cost + 1:
				cost[next_x][next_y] = current_cost + 1
				parrent[next_x][next_y] = current_point
				
				if [next_x, next_y] == ending_point:
					found = True
					break

				frontier.put(cost[next_x][next_y] ,[next_x, next_y])

	if not found:
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
	return answer

def ucs(graph, starting_point, ending_point, mode, callback, 
		teleport_list = [], bonus_point_list = [], itermediate_point_list = []):

	if not isValidGraph(graph):
		return None

	if mode == AlgorithmsMode.NORMAL:
		return __normal_ucs(graph, starting_point, ending_point, callback)

	if mode == AlgorithmsMode.BONUS_POINT:
		return __ucs_with_bonus_point(graph, starting_point, ending_point, bonus_point_list, callback)

	if mode == AlgorithmsMode.INTERMEDIATE_POINT:
		return __ucs_intermediate_point(graph, starting_point, ending_point, itermediate_point_list, callback)

	if mode == AlgorithmsMode.TELEPORT_POINT:
		return __ucs_with_teleport_point(graph, starting_point, ending_point, teleport_list, callback)
