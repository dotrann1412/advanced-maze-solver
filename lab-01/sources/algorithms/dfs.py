from algorithms.algorithms_utils import *
from constants import *
from utils import manhattan_distance
from visualizer import set_path_color, set_frontier_color
from datetime import datetime

def __normal_dfs(graph, starting_point, ending_point):
	size = graph_size(graph)

	visited = [[False for __ in range(size[1])] for _ in range(size[0])]
	path = []
	
	def __process(current_position, depth = 0):
		if ending_point == current_position:
			return True

		if current_position != starting_point:
			set_frontier_color(current_position[1], current_position[0])
		
		visited[current_position[0]][current_position[1]] = True

		for element in direction:
			next_x, next_y = current_position[0] + element[0], current_position[1] + element[1]

			if not is_in_graph(graph, [next_x, next_y]) or graph[next_x][next_y] == MazeObject.WALL \
				or visited[next_x][next_y]:
				continue

			if __process((next_x, next_y), depth + 1):
				path.append((next_x, next_y))
				return True
		
		return False

	found = __process(starting_point)

	if not found:
		return None

	path.append(starting_point)
	path = path[::-1]

	set_path_color(path)
	
	return len(path) - 1


def __dfs_with_bonus_point(graph, starting_point, ending_point, bonus_points):
	return __normal_dfs(graph, starting_point, ending_point)


def __dfs_intermediate_point(graph, starting_point, ending_point, intermediate_points):
	intermediate_list = list(intermediate_points.keys())

	def choose(_starting_point, destinations):
		good = destinations[0]
		for point in destinations[1:]:
			if manhattan_distance(good, _starting_point) > manhattan_distance(good, point):
				good = point
		return good

	current_position = starting_point
	
	path = []
	while len(intermediate_list) != 0:
		destination = choose(current_position, intermediate_list)
		intermediate_list.remove(destination)
		path += __normal_dfs(graph, current_position, destination)
		current_position = destination

	path += __normal_dfs(graph, current_position, ending_point)
	return len(path) - 1


def __dfs_with_teleport_point(graph, starting_point, ending_point, teleport_points):
	size = graph_size(graph)

	if starting_point[0] < 0 or starting_point[0] >= size[0] or starting_point[1] < 0 or starting_point[1] >= size[1]:
		return None

	special_points = set([starting_point, ending_point] + list(teleport_points.keys()))
	visited = [[False for __ in range(size[1])] for _ in range(size[0])]
	path = []

	def __process(current_position, tele = False):
		if current_position == ending_point:
			return True

		if current_position not in special_points:
			set_frontier_color(current_position[1], current_position[0])

		visited[current_position[0]][current_position[1]] = True

		for element in direction:
			next_x, next_y = current_position[0] + element[0], current_position[1] + element[1]

			if not is_in_graph(graph, [next_x, next_y]) or graph[next_x][next_y] == MazeObject.WALL \
				or visited[next_x][next_y]:
				continue

			if (next_x, next_y) in teleport_points:
				dest_x, dest_y = teleport_points[(next_x, next_y)]
				if not visited[dest_x][dest_y] and __process((dest_x, dest_y)):
					path.append((dest_x, dest_y))
					return True

			if __process((next_x, next_y)):
				path.append((next_x, next_y))
				return True

		
		return False

	found = __process(starting_point)

	if not found:
		return None

	path = path[::-1]

	set_path_color(path, special_points)

	return len(path) - 1


def dfs(graph, starting_point, ending_point, mode, bonus_points, intermediate_points, teleport_points, hf=None):
	if mode == AlgorithmsMode.NORMAL:
		starting_time_point = datetime.now()
		cost = __normal_dfs(graph, starting_point, ending_point)
		ending_time_point = datetime.now()
		print('[*][DFS] Normal mode')
	
	elif mode == AlgorithmsMode.BONUS:
		starting_time_point = datetime.now()
		cost = __dfs_with_bonus_point(graph, starting_point, ending_point, bonus_points)

		ending_time_point = datetime.now()
		print('[*][DFS] Bonus mode')

	elif mode == AlgorithmsMode.INTERMEDIATE:
		starting_time_point = datetime.now()
		cost = __dfs_intermediate_point(graph, starting_point, ending_point, intermediate_points)
		ending_time_point = datetime.now()
		print('[*][DFS] Intermediate mode')

	elif mode == AlgorithmsMode.TELEPORT:
		starting_time_point = datetime.now()
		cost = __dfs_with_teleport_point(graph, starting_point, ending_point, teleport_points)
		ending_time_point = datetime.now()
		print('[*][DFS] Teleport mode')
	
	else:
		print('[*][DFS] Unknown mode')
		return None

	print(f'\tCost = {cost}, Time = {ending_time_point - starting_time_point}')
	return cost
