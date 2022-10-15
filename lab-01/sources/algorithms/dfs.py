from algorithms.algorithms_utils import *
from constants import *
from utils import manhattan_distance

def __normal_dfs(graph, starting_point, ending_point, callback):
	size = grapthSize(graph)

	visited = [[False for __ in range(size[1])] for _ in range(size[0])]
	path = []
	
	def __process(current_position, depth = 0):
		if ending_point == current_position:
			return True

		if current_position != starting_point:
			callback(current_position[1], current_position[0], Colors.FRONTIER_COLOR)
		
		visited[current_position[0]][current_position[1]] = True

		for element in direction:
			next_x, next_y = current_position[0] + element[0], current_position[1] + element[1]

			if not isInGraph(graph, [next_x, next_y]) or graph[next_x][next_y] == MazeObject.WALL \
				or visited[next_x][next_y]:
				continue

			if __process((next_x, next_y), depth + 1):
				path.append((next_x, next_y))
				return True
		
		return False

	found = __process(starting_point)

	if not found:
		return None

	for point in path[1:]:
		callback(point[1], point[0], Colors.PATH_COLOR)
	
	return path[::-1]

def __dfs_with_bonus_point(graph, starting_point, ending_point, bonus_points, callback):
	return __normal_dfs(graph, starting_point, ending_point, callback)

def __dfs_intermediate_point(graph, starting_point, ending_point, intermediate_points, callback):
	def choose(_starting_point, destinations):
		good = destinations[0]
		for point in destinations[1:]:
			if manhattan_distance(good, _starting_point) > manhattan_distance(good, point):
				good = point
		return good

	current_position = starting_point
	
	path = []
	while len(intermediate_points) != 0:
		destination = choose(current_position, intermediate_points)
		intermediate_points.remove(destination)
		path += __normal_dfs(graph, current_position, destination, callback)
		current_position = destination

	path += __normal_dfs(graph, current_position, ending_point, callback)
	return path

def __dfs_with_teleport_point(graph, starting_point, ending_point, teleport_points, callback):
	size = grapthSize(graph)
	
	if starting_point[0] < 0 or starting_point[0] >= size[0] or starting_point[1] < 0 or starting_point[1] >= size[1]:
		return None

	visited = [[False for __ in range(size[1])] for _ in range(size[0])]
	path = []

	def __process(current_position, tele = False):
		if current_position == ending_point:
			return True

		if current_position != starting_point:
			callback(current_position[1], current_position[0], Colors.FRONTIER_COLOR)

		visited[current_position[0]][current_position[1]] = True

		for element in direction:
			next_x, next_y = current_position[0] + element[0], current_position[1] + element[1]

			if not isInGraph(graph, [next_x, next_y]) or graph[next_x][next_y] == MazeObject.WALL \
				or visited[next_x][next_y]:
				continue

			if (next_x, next_y) in teleport_points:
				destination_x, destination_y = teleport_points[(next_x, next_y)]
				if not visited[destination_x][destination_y] and __process(*teleport_points[next_x, next_y]):
					path.append((destination_x, destination_y))
					return True

			if __process((next_x, next_y)):
				path.append((next_x, next_y))
				return True

		
		return False

	found = __process(starting_point)

	if not found:
		return None

	for point in path[1:]:
		callback(point[1], point[0], Colors.PATH_COLOR)

	return path[::-1]

def dfs(graph, starting_point, ending_point, mode, bonus_points, intermediate_points, teleport_points, call_back, hf=None):
	
	if mode == AlgorithmsMode.NORMAL:
		return __normal_dfs(graph, starting_point, ending_point, call_back)

	if mode == AlgorithmsMode.BONUS_POINT:
		return __dfs_with_bonus_point(graph, starting_point, ending_point, bonus_points, call_back)
	
	if mode == AlgorithmsMode.INTERMEDIATE_POINT:
		return __dfs_intermediate_point(graph, starting_point, ending_point, intermediate_points, call_back)
	
	if mode == AlgorithmsMode.TELEPORT_POINT:
		return __dfs_with_teleport_point(graph, starting_point, ending_point, teleport_points, call_back)
