from algorithms.algorithms_utils import *
from constants import *

def __normal_dfs(graph, starting_point, ending_point, callback):
	size = grapthSize(graph)

	visited = [[False for __ in range(size[1])] for _ in range(size[0])]
	answer = []
	
	print(graph, starting_point, ending_point)
	def __process(current_position, depth = 0):
		print(depth, current_position)
		if ending_point == current_position:
			return True

		if current_position != starting_point:
			callback(current_position[1], current_position[0], Colors.PATH_COLOR)
		
		visited[current_position[0]][current_position[1]] = True

		for element in direction:
			next_x, next_y = current_position[0] + element[0], current_position[1] + element[1]

			next_char = graph[next_x][next_y]
			if not isInGraph(graph, [next_x, next_y]) or not isEmptyCell(next_char) \
				or visited[next_x][next_y]:
				continue

			if __process((next_x, next_y), depth + 1):
				answer.append((next_x, next_y))
				return True

		# visited[current_position[0]][current_position[1]] = False
		callback(current_position[1], current_position[0], Colors.WHITE)
		
		return False

	found = __process(starting_point)

	if not found:
		return None
	
	print(answer)
	return answer[::-1]

def __dfs_with_bonus_point(graph, starting_point, ending_point, bonus_points, callback):
	def __process(current_position):
		pass

def __dfs_intermediate_point(graph, starting_point, ending_point, itermediate_points, callback):
	def __process(current_position):
		pass

def __dfs_with_teleport_point(graph, starting_point, ending_point, teleport_points, callback):
	size = grapthSize(graph)
	
	if starting_point[0] < 0 or starting_point[0] >= size[0] or starting_point[1] < 0 or starting_point[1] >= size[1]:
		return None

	visited = [[False for __ in range(size[1])] for _ in range(size[0])]
	answer = []

	def __process(current_position, tele = False):
		if current_position == ending_point:
			return True

		if current_position != starting_point:
			callback(current_position[1], current_position[0], Colors.PATH_COLOR)

		visited[current_position[0]][current_position[1]] = True

		for element in direction:
			next_x, next_y = current_position[0] + element[0], current_position[1] + element[1]

			next_char = graph[next_x][next_y]
			if not isInGraph(graph, [next_x, next_y]) or not isEmptyCell(next_char) \
				or visited[next_x][next_y]:
				continue

			if (next_x, next_y) in teleport_points:
				for x, y in teleport_points:
					if not visited[x][y]:
						if __process((x, y)):
							answer.append((next_x, next_y))
							return True

			if __process((next_x, next_y)):
				answer.append((next_x, next_y))
				return True

		callback(current_position[1], current_position[0], Colors.WHITE)
		
		return False

	found = __process(starting_point)

	if not found:
		return None

	return answer[::-1]

def dfs(graph, starting_point, ending_point, mode, bonus_points, intermediate_points, teleport_points, call_back, hf=None):
	
	if mode == AlgorithmsMode.NORMAL:
		return __normal_dfs(graph, starting_point, ending_point, call_back)

	if mode == AlgorithmsMode.BONUS_POINT:
		return __dfs_with_bonus_point(graph, starting_point, ending_point, bonus_points, call_back)
	
	if mode == AlgorithmsMode.INTERMEDIATE_POINT:
		return __dfs_intermediate_point(graph, starting_point, ending_point, intermediate_points, call_back)
	
	if mode == AlgorithmsMode.TELEPORT_POINT:
		return __dfs_with_teleport_point(graph, starting_point, ending_point, teleport_points, call_back)
