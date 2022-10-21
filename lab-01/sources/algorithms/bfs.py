from algorithms.algorithms_utils import *
from constants import *
from utils import manhattan_distance
from visualizer import set_path_color, set_frontier_color
from datetime import datetime

def __normal_bfs(graph, starting_point, ending_point):
	size = [len(graph), len(graph[0])]
	frontier = []

	if starting_point[0] < 0 or starting_point[0] >= size[0] or starting_point[1] < 0 or starting_point[1] >= size[1]:
		return None

	parent = [[None for __ in range(size[1])] for _ in range(size[0])]
	
	frontier.append(starting_point)
	parent[starting_point[0]][starting_point[1]] = starting_point
	
	found = False

	while len(frontier) != 0 and not found:
		current = frontier[0]
		frontier.pop(0)

		if current != starting_point:
			set_frontier_color(current[1], current[0])

		for element in direction:
			next_x, next_y = current[0] + element[0], current[1] + element[1]
			
			if not is_in_graph(graph, (next_x, next_y)) or parent[next_x][next_y] or graph[next_x][next_y] == MazeObject.WALL:
				continue

			if (next_x, next_y) == ending_point:
				parent[next_x][next_y] = current
				found = True
				break

			parent[next_x][next_y] = current
			frontier.append((next_x, next_y))

	if not ending_point or not parent[ending_point[0]][ending_point[1]]:
		return None

	answer = []
	pointer = ending_point

	limit = size[0] * size[1]

	while pointer != starting_point:
		answer.append(pointer)
		pointer = parent[pointer[0]][pointer[1]]

		limit -= 1
		if limit == 0:
			raise Exception("Infinite loop!")

	answer.append(starting_point)
	answer = answer[::-1]

	set_path_color(answer)
	
	return len(answer) - 1


def __bfs_with_bonus_point(graph, starting_point, ending_point, bonus_points):
	# bfs is a uniform cost search --> this mode is not really available
	return __normal_bfs(graph, starting_point, ending_point)


def __bfs_intermediate_point(graph, starting_point, ending_point, intermediate_points):
	intermediate_list = list(intermediate_points.keys())

	def pick_next_bonus(_starting_point, destinations):
		good = destinations[0]
		for point in destinations[1:]:
			if manhattan_distance(good, _starting_point) > manhattan_distance(good, point):
				good = point
		return good

	current_position = starting_point
	
	path = []
	while len(intermediate_list) != 0:
		destination = pick_next_bonus(current_position, intermediate_list)
		intermediate_list.remove(destination)
		path += __normal_bfs(graph, current_position, destination)
		current_position = destination

	path += __normal_bfs(graph, current_position, ending_point)

	return len(path) - 1


def __bfs_with_teleport_point(graph, starting_point, ending_point, teleport_points: dict):
	size = [len(graph), len(graph[0])]
 
	frontier = []
	parent = [[None for __ in range(size[1])] for _ in range(size[0])]
	
	frontier.append(starting_point)
	parent[starting_point[0]][starting_point[1]] = starting_point
	
	found = False
	special_points = set([starting_point, ending_point] + list(teleport_points.keys()))

	while len(frontier) != 0 and not found:
		current = frontier[0]
		frontier.pop(0)

		if current not in special_points:
			set_frontier_color(current[1], current[0])
			
		for element in direction:
			next_x, next_y = current[0] + element[0], current[1] + element[1]
			if not is_in_graph(graph, (next_x, next_y)) or graph[next_x][next_y] == MazeObject.WALL or parent[next_x][next_y] is not None:
				continue

			if (next_x, next_y) == ending_point:
				parent[next_x][next_y] = current
				found = True
				break

			if (next_x, next_y) in teleport_points:
				destination_x, destination_y = teleport_points[(next_x, next_y)]

				if (destination_x, destination_y) == ending_point:
					parent[destination_x][destination_y] = current
					found = True
					break

				if not parent[destination_x][destination_y]:
					parent[destination_x][destination_y] = current
					frontier.append((destination_x, destination_y))

			parent[next_x][next_y] = current
			frontier.append((next_x, next_y))

	if not ending_point or not parent[ending_point[0]][ending_point[1]]:
		return None

	answer = []
	pointer = ending_point

	limit = size[0] * size[1]

	while pointer != starting_point:
		answer.append(pointer)
		pointer = parent[pointer[0]][pointer[1]]

		limit -= 1
		if limit == 0:
			raise Exception("Infinite loop!")

	answer.append(starting_point)
	answer = answer[::-1]
	set_path_color(answer, special_points)

	return len(answer) - 1


def bfs(graph, starting_point, ending_point, mode, bonus_points, intermediate_points, teleport_points, hf=None):
	if mode == AlgorithmsMode.NORMAL:
		starting_time_point = datetime.now()
		cost = __normal_bfs(graph, starting_point, ending_point)
		ending_time_point = datetime.now()
		print('[*][BFS] Normal mode')
	
	elif mode == AlgorithmsMode.BONUS:
		starting_time_point = datetime.now()
		cost = __bfs_with_bonus_point(graph, starting_point, ending_point, bonus_points)

		ending_time_point = datetime.now()
		print('[*][BFS] Bonus mode')

	elif mode == AlgorithmsMode.INTERMEDIATE:
		starting_time_point = datetime.now()
		cost = __bfs_intermediate_point(graph, starting_point, ending_point, intermediate_points)
		ending_time_point = datetime.now()
		print('[*][BFS] Intermediate mode')

	elif mode == AlgorithmsMode.TELEPORT:
		starting_time_point = datetime.now()
		cost = __bfs_with_teleport_point(graph, starting_point, ending_point, teleport_points)
		ending_time_point = datetime.now()
		print('[*][BFS] Teleport mode')
	
	else:
		print('[*][BFS] Unknown mode')
		return None

	print(f'\tCost = {cost}, Time = {ending_time_point - starting_time_point}')
	return cost
