from algorithms.algorithms_utils import *
from queue import PriorityQueue
from constants import *
from utils import manhattan_distance
from visualizer import set_path_color, set_frontier_color, set_color

def __trace_back(parent, starting_point, ending_point, limit = INF):
	path = []
	pointer = ending_point

	while pointer != starting_point:
		path.append(pointer)
		print('[DEBUG]',pointer)
		pointer = parent[pointer[0]][pointer[1]]

		limit -= 1
		if limit == 0:
			raise Exception("Infinite loop!")
	
	return path[::-1]

def __normal_ucs(graph, starting_point, ending_point):
	frontier = PriorityQueue()
	size = graph_size(graph)
	sleep_time = calc_sleep_time(size)

	parent = [[None for __ in range(size[1])] for _ in range(size[0])]
	cost = [[INF for __ in range(size[1])] for _ in range(size[0])]

	frontier.put((0, starting_point))
	cost[starting_point[0]][starting_point[1]] = 0
	parent[starting_point[0]][starting_point[1]] = starting_point

	found = False
	
	while not frontier.empty() and not found:
		current_cost, current_point = frontier.get()
		if cost[current_point[0]][current_point[1]] != current_cost:
			continue
		
		if current_point != starting_point:
			set_frontier_color(current_point[1], current_point[0], sleep_time)

		for dir in direction:
			next_x, next_y = current_point[0] + dir[0], current_point[1] + dir[1]

			if not is_in_graph(graph, (next_x, next_y)) or graph[next_x][next_y] == MazeObject.WALL:
				continue

			if (next_x, next_y) == ending_point:
				parent[next_x][next_y] = current_point
				found = True
				break

			if cost[next_x][next_y] > current_cost + 1:
				cost[next_x][next_y] = current_cost + 1
				parent[next_x][next_y] = current_point
				frontier.put((current_cost + 1, (next_x, next_y)))

	if not found:
		return None
	
	path = [starting_point] + __trace_back(parent, starting_point, ending_point, limit = size[0] * size[1])

	set_path_color(path, sleep_time)

	return path

def __ucs_with_bonus_point(graph, starting_point, ending_point, bonus_points):
	frontier = PriorityQueue()
	
	size = graph_size(graph)
	sleep_time = calc_sleep_time(size)

	bonus_points_cp = bonus_points.copy()

	frontier.put((0, starting_point))
	parent = [[None for _ in range(size[1])] for __ in range(size[0])]
	cost = [[INF for _ in range(size[1])] for __ in range(size[0])]

	parent[starting_point[0]][starting_point[1]] = starting_point
	cost[starting_point[0]][starting_point[1]] = 0

	path_to_bonus = {}
	special_points = [starting_point, ending_point] + list(bonus_points.keys())
	def __trace_back_bonus(point):
		pointer = point
		path = [point]
		while True:
			pointer = parent[pointer[0]][pointer[1]]
			path.append(pointer)
			check = True

			for d in direction:
				par_next_x, par_next_y = pointer[0] + d[0], pointer[1] + d[1]
				if cost[par_next_x][par_next_y] < cost[pointer[0]][pointer[1]]:
					check = False
					break

			if check:
				break

		return path[::-1]

	while not frontier.empty():
		current_cost, current_point = frontier.get()

		if current_point != starting_point:
			set_frontier_color(current_point[1], current_point[0], sleep_time)

		if current_cost != cost[current_point[0]][current_point[1]]:
			continue

		for d in direction:
			next_x, next_y = current_point[0] + d[0], current_point[1] + d[1]

			if not is_in_graph(graph, (next_x, next_y)) or graph[next_x][next_y] == MazeObject.WALL:
				continue

			bonus = bonus_points_cp.pop((next_x, next_y), 0)

			if cost[next_x][next_y] > current_cost + 1 + bonus:
				cost[next_x][next_y] = current_cost + 1 + bonus
				parent[next_x][next_y] = current_point
				frontier.put((current_cost + 1 + bonus , (next_x, next_y)))
				
				if bonus != 0:
					path_to_bonus[(next_x, next_y)] = __trace_back_bonus((next_x, next_y))

	if parent[ending_point[0]][ending_point[1]] == None:
		return None

	print('[*] Cost: ', cost[ending_point[0]][ending_point[1]])
	path = __trace_back_bonus(ending_point)
	magican = path[0]

	while magican != starting_point:
		path = path_to_bonus[magican] + path[1:]
		magican = path[0]
	
	for bonus in bonus_points:
		set_color(bonus[1], bonus[0], Colors.SPECIAL, 0)

	set_path_color(path, sleep_time, bonus_points)
	
	print(path)

	return path

def __ucs_intermediate_point(graph, starting_point, ending_point, intermediate_points):
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
		path += __normal_ucs(graph, current_position, destination)
		current_position = destination

	path += __normal_ucs(graph, current_position, ending_point)
	return path

def __ucs_with_teleport_point(graph, starting_point, ending_point, teleport_points):
	frontier = PriorityQueue()
	size = graph_size(graph)
	sleep_time = calc_sleep_time(size)

	parent = [[None for __ in range(size[1])] for _ in range(size[0])]
	cost = [[INF for __ in range(size[1])] for _ in range(size[0])]

	frontier.put((0, starting_point))
	cost[starting_point[0]][starting_point[1]] = 0
	parent[starting_point[0]][starting_point[1]] = starting_point
	special_points = set([starting_point, ending_point] + list(teleport_points.keys()))

	found = False
	while not frontier.empty() and not found:
		current_cost, current_point = frontier.get()

		if cost[current_point[0]][current_point[1]] != current_cost:
			continue # this is an outdated state in frontier

		if current_point not in special_points:
			set_frontier_color(current_point[1], current_point[0], sleep_time // 5)
		
		for dir in direction:
			next_x, next_y = current_point[0] + dir[0], current_point[1] + dir[1]
			
			if is_in_graph(graph, (next_x, next_y)) or graph[next_x][next_y] == MazeObject.WALL:
				continue

			# this mode is an informed cost mode 
			#	 --> we can terminate the process in the first time meet the destination
			if (next_x, next_y) == ending_point:
				found = True
				parent[next_x][next_y] = current_point
				break

			if (next_x, next_y) in teleport_points:
				destination_x, destination_y = teleport_points[(next_x, next_y)]

				if (destination_x, destination_y) == ending_point:
					found = True
					parent[destination_x][destination_y] = current_point
					break

				if cost[destination_x][destination_y] > current_cost + 1:
					cost[destination_x][destination_y] = current_cost + 1
					parent[destination_x][destination_y] = current_point
					frontier.put((current_cost + 1, (destination_x, destination_y)))
			
			if cost[next_x][next_y] > current_cost + 1:
				cost[next_x][next_y] = current_cost + 1
				parent[next_x][next_y] = current_point
				frontier.put((current_cost + 1 , (next_x, next_y)))

	if not found:
		return None
	
	path = __trace_back(parent, starting_point, ending_point, limit = size[0] * size[1])

	set_path_color(path, sleep_time, special_points)

	return path

def ucs(graph, starting_point, ending_point, mode, bonus_points, intermediate_points, teleport_points, hf=None):
	from datetime import datetime
	
	if mode == AlgorithmsMode.NORMAL:
		print('[*][UCS] Normal mode')
		return __normal_ucs(graph, starting_point, ending_point)

	if mode == AlgorithmsMode.BONUS_POINT:
		print('[*][UCS] Bonus mode')
		starting_time_point = datetime.now()
		path = __ucs_with_bonus_point(graph, starting_point, ending_point, bonus_points)
		print('[*] Time duration: ', datetime.now() - starting_time_point, ' second(s)')
		return path


	if mode == AlgorithmsMode.INTERMEDIATE_POINT:
		print('[*][UCS] Intermediate mode')
		return __ucs_intermediate_point(graph, starting_point, ending_point, intermediate_points)

	
	
	if mode == AlgorithmsMode.TELEPORT_POINT:
		print('[*][UCS] Teleport mode')
		return __ucs_with_teleport_point(graph, starting_point, ending_point, teleport_points)