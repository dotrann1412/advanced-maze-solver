from algorithms.algorithms_utils import *
from queue import PriorityQueue
from constants import *
from utils import manhattan_distance

def __trace_back(parent, starting_point, ending_point, limit = INF):
	path = []
	pointer = ending_point

	while pointer != starting_point and pointer != parent[parent[pointer[0]][pointer[1]][0]][parent[pointer[0]][pointer[1]][1]]:
		path.append(pointer)
		print('[DEBUG]',pointer)
		pointer = parent[pointer[0]][pointer[1]]

		limit -= 1
		if limit == 0:
			raise Exception("Infinite loop!")
	
	return path[::-1]

def __normal_ucs(graph, starting_point, ending_point, callback):
	frontier = PriorityQueue()
	size = grapthSize(graph)
	
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
			callback(current_point[1], current_point[0], Colors.FRONTIER_COLOR)

		for dir in direction:
			next_x, next_y = current_point[0] + dir[0], current_point[1] + dir[1]

			if not isInGraph(graph, (next_x, next_y)) or graph[next_x][next_y] == MazeObject.WALL:
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
	
	path = __trace_back(parent, starting_point, ending_point, limit = size[0] + size[1])

	
	for point in path:
		callback(point[1], point[0], Colors.PATH_COLOR)
	
	
	return path

def __ucs_with_bonus_point(graph, starting_point, ending_point, bonus_points, callback):
	frontier = PriorityQueue()
	
	size = grapthSize(graph)

	bonus_dict = {}
	for x, y, bonus in bonus_points:
		bonus_dict[(x, y)] = bonus

	frontier.put((0, starting_point))
	parent = [[None for _ in range(size[1])] for __ in range(size[0])]
	cost = [[INF for _ in range(size[1])] for __ in range(size[0])]

	parent[starting_point[0]][starting_point[1]] = starting_point
	cost[starting_point[0]][starting_point[1]] = 0

	path_to_bonus = {}

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

		if current_point != starting_point and current_point not in path_to_bonus and current_point not in bonus_dict and current_point != ending_point:
			callback(current_point[1], current_point[0], Colors.FRONTIER_COLOR)

		if current_cost != cost[current_point[0]][current_point[1]]:
			continue

		for d in direction:
			next_x, next_y = current_point[0] + d[0], current_point[1] + d[1]

			if not isInGraph(graph, (next_x, next_y)) or graph[next_x][next_y] == MazeObject.WALL:
				continue

			bonus = bonus_dict.pop((next_x, next_y), 0)

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
		path = path_to_bonus[magican] + path
		magican = path[0]
	
	for point in path[1:-1]:
		if point not in path_to_bonus:
			callback(point[1], point[0], Colors.PATH_COLOR, 10)
	
	print(path)

	return path

def __ucs_intermediate_point(graph, starting_point, ending_point, intermediate_points, callback):
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
		path += __normal_ucs(graph, current_position, destination, callback)
		current_position = destination

	path += __normal_ucs(graph, current_position, ending_point, callback)
	return path

def __ucs_with_teleport_point(graph, starting_point, ending_point, teleport_points, callback):
	frontier = PriorityQueue()
	size = grapthSize(graph)
	
	parent = [[None for __ in size[1]] for _ in size[0]]
	cost = [[INF for __ in size[1]] for _ in size[0]]

	frontier.put([0, starting_point])
	cost[starting_point[0]][starting_point[1]] = 0
	parent[starting_point[0]][starting_point[1]] = starting_point

	closed_bonus_point = []

	found = False
	while not frontier.empty() and not found:
		current_cost, current_point = frontier.get()

		if cost[current_point[0]][current_point[1]] != current_cost:
			continue # this is a outdate state in frontier

		if current_point != starting_point:
			callback(current_point[1], current_point[0], Colors.FRONTIER_COLOR)
		
		for dir in direction:
			next_x, next_y = current_point[0] + dir[0], current_point[1] + dir[1]
			
			if isInGraph(graph, (next_x, next_y)) or graph[next_x][next_y] == MazeObject.WALL:
				continue

			# this mode is an infomed cost mode 
			#	 --> we can terminate the process in the first time meet the destination
			if (destination_x, destination_y) == ending_point:
				found = True
				break

			if (next_x, next_y) in teleport_points:
				destination_x, destination_y = teleport_points[(next_x, next_y)]

				if (destination_x, destination_y) == ending_point:
					found = True
					break

				if cost[destination_x][destination_y] > current_cost + 1:
					cost[destination_x][destination_y] = current_cost + 1
					parent[destination_x][destination_y] = current_point
					frontier.put(cost[destination_x][destination_y], (next_x, next_y))
			
			if cost[next_x][next_y] > current_cost + 1:
				cost[next_x][next_y] = current_cost + 1
				parent[next_x][next_y] = current_point
				frontier.put(cost[next_x][next_y] , (next_x, next_y))

	if not found:
		return None
	
	path = __trace_back(parent, starting_point, ending_point, limit = size[0] + size[1])

	for point in path[1:-1]:
		callback(point[1], point[0], Colors.PATH_COLOR)

	return path

def ucs(graph, starting_point, ending_point, mode, bonus_points, intermediate_points, teleport_points, call_back, hf=None):
	from datetime import datetime
	
	if mode == AlgorithmsMode.NORMAL:
		print('[*][UCS] Normal mode')
		return __normal_ucs(graph, starting_point, ending_point, call_back)

	if mode == AlgorithmsMode.BONUS_POINT:
		print('[*][UCS] Bonus mode')
		starting_time_point = datetime.now()
		path = __ucs_with_bonus_point(graph, starting_point, ending_point, bonus_points, call_back)
		print('[*] Time duration: ', datetime.now() - starting_time_point, ' second(s)')
		return path


	if mode == AlgorithmsMode.INTERMEDIATE_POINT:
		print('[*][UCS] Intermediate mode')
		return __ucs_intermediate_point(graph, starting_point, ending_point, intermediate_points, call_back)

	
	
	if mode == AlgorithmsMode.TELEPORT_POINT:
		print('[*][UCS] Teleport mode')
		return __ucs_with_teleport_point(graph, starting_point, ending_point, teleport_points, call_back)