from algorithms.algorithms_utils import *
from constants import *
from utils import manhattan_distance
from queue import PriorityQueue
from visualizer import set_path_color, set_frontier_color
import copy
from datetime import datetime

def __normal_gbfs(graph, start, end, hf):
	def h(point):
		return hf(point, end)
	terminated = [-1, -1]
	dim = graph_size(graph)
	priority_queue = PriorityQueue()

	if not is_in_graph(graph, start):
		return None

	parent = [[None for __ in range(dim[1])] for _ in range(dim[0])]

	priority_queue.put((h(start), start))
	parent[start[0]][start[1]] = terminated

	found = False
	
	while not priority_queue.empty() and not found:
		_h, current = priority_queue.get()


		if current != start and current:
			set_frontier_color(current[1], current[0])

		for element in direction:
			next_step_x, next_step_y = current[0] + element[0], current[1] + element[1]

			if not is_in_graph(graph, (next_step_x, next_step_y)) or graph[next_step_x][next_step_y] == MazeObject.WALL or parent[next_step_x][next_step_y]:
				continue


			if (next_step_x, next_step_y)  == end:
				parent[end[0]][end[1]] = current
				found = True
				break
			
			parent[next_step_x][next_step_y] = current
			priority_queue.put((h((next_step_x, next_step_y)) ,(next_step_x, next_step_y )))
		
		if current != start:
			set_frontier_color(current[1], current[0])

	if not end or not parent[end[0]][end[1]]:
		return None

	answer = []
	pointer = end

	while parent[pointer[0]][pointer[1]] != terminated:
		answer.append(pointer)
		pointer = parent[pointer[0]][pointer[1]]
	answer.append(start)
	
	answer = answer[::-1]

	set_path_color(answer, [start, end])

	return len(answer) - 1

def __gbfs_with_bonus_point(graph, start, end, bonus_points, heuristic):
	size = graph_size(graph)
	special_points = set([start, end] + list(bonus_points.keys()))
	special_points_for_rendering = copy.deepcopy(special_points)
	
	def __extra_heuristic(point):
		val = INF
		for p in special_points:
			val = min(val, heuristic(p, end) + (bonus_points[p] if (p in bonus_points and p != point) else 0) + heuristic(point, p)) 
		return val
	
	frontier = PriorityQueue()
	frontier.put((__extra_heuristic(start), start))
	parent = [[None for __ in range(size[1])] for _ in range(size[0])]
	cost = [[INF for __ in range(size[1])] for _ in range(size[0])]

	parent[start[0]][start[1]] = parent
	cost[start[0]][start[1]] = 0

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
		_hf, current = frontier.get()

		if current not in special_points:
			set_frontier_color(current[1], current[0])

		for d in direction:
			next_x, next_y = current[0] + d[0], current[1] + d[1]
			
			if not is_in_graph(graph, (next_x, next_y)) or graph[next_x][next_y] == MazeObject.WALL: # or parent[next_x][next_y] is not None:
				continue

			if (next_x, next_y) == end:
				parent[next_x][next_y] = current
				cost[next_x][next_y] = cost[current[0]][current[1]] + 1
				break 
			
			bonus = bonus_points.get((next_x, next_y), 0)
			if cost[next_x][next_y] > cost[current[0]][current[1]] + bonus + 1:
				cost[next_x][next_y] = cost[current[0]][current[1]] + bonus + 1
				parent[next_x][next_y] = current
				frontier.put((__extra_heuristic((next_x, next_y)), (next_x, next_y)))

				if bonus != 0:
					bonus_points.pop((next_x, next_y))
					special_points.remove((next_x, next_y))
					path_to_bonus[(next_x, next_y)] = __trace_back_bonus((next_x, next_y))

	if parent[end[0]][end[1]] == None:
		return None

	path = __trace_back_bonus(end)
	magican = path[0]

	while magican != start:
		path = path_to_bonus[magican] + path[1:]
		magican = path[0]

	set_path_color(path, special_points_for_rendering)
	
	return len(path) - 1


def __gbfs_with_intermediate_point(graph, start, end, intermediate_points, hf):
	pass

def __gbfs_with_teleport_point(graph, start, end, teleport_points: dict, heuristic):
	terminated = [-1, -1]
	size = graph_size(graph)

	priority_queue = PriorityQueue()
	special_points = [end] + list(teleport_points.keys())

	def __extra_heuristic(point):
		val = INF
		for p in special_points:
			val = min(val, heuristic(p, end) + heuristic(point, p))
			if p in teleport_points:
				val = min(val, heuristic(teleport_points[p], end) + heuristic(point, p))
		return val

	if not is_in_graph(graph, start):
		return None

	parent = [[None for __ in range(size[1])] for _ in range(size[0])]

	priority_queue.put((__extra_heuristic(start), start))
	parent[start[0]][start[1]] = terminated

	found = False
	while not priority_queue.empty() and not found:
		hf, current = priority_queue.get()
		
		if current != start and current not in teleport_points:
			set_frontier_color(current[1], current[0])
		
		for d in direction:
			next_x, next_y = current[0] + d[0], current[1] + d[1]

			if not is_in_graph(graph, (next_x, next_y)) or graph[next_x][next_y] == MazeObject.WALL or parent[next_x][next_y] is not None:
				continue

			if (next_x, next_y) == end:
				parent[end[0]][end[1]] = current
				found = True
				break

			if (next_x, next_y) in teleport_points:
				destination_x, destination_y = teleport_points[(next_x, next_y)]
				if not parent[destination_x][destination_y]:
					parent[destination_x][destination_y] = current
					priority_queue.put((__extra_heuristic((destination_x, destination_y)), (destination_x, destination_y)))
			
			parent[next_x][next_y] = current
			priority_queue.put((__extra_heuristic((next_x, next_y)) , (next_x, next_y)))

	if not end or not parent[end[0]][end[1]]:
		return None
	
	answer = []
	pointer = end

	while parent[pointer[0]][pointer[1]] != terminated:
		answer.append(pointer)
		pointer = parent[pointer[0]][pointer[1]]

	answer.append(start)
	answer = answer[::-1]

	set_path_color(answer)

	return len(answer) - 1
	

def gbfs(graph, start, end, mode, bonus_points, intermediate_points, teleport_points, hf=manhattan_distance):
	if mode == AlgorithmsMode.NORMAL:
		starting_time_point = datetime.now()
		cost = __normal_gbfs(graph, start, end, hf)
		ending_time_point = datetime.now()
		print('[*][GBFS] Normal mode')
	
	elif mode == AlgorithmsMode.BONUS:
		starting_time_point = datetime.now()
		cost = __gbfs_with_bonus_point(graph, start, end, bonus_points, hf)
		ending_time_point = datetime.now()
		print('[*][GBFS] Bonus mode')

	elif mode == AlgorithmsMode.INTERMEDIATE:
		starting_time_point = datetime.now()
		cost = __gbfs_with_intermediate_point(graph, start, end, intermediate_points, hf)
		ending_time_point = datetime.now()
		print('[*][GBFS] Intermediate mode')

	elif mode == AlgorithmsMode.TELEPORT:
		starting_time_point = datetime.now()
		cost = __gbfs_with_teleport_point(graph, start, end, teleport_points, hf)
		ending_time_point = datetime.now()
		print('[*][GBFS] Teleport mode')
	
	else:
		print('[*][GBFS] Unknown mode')
		return None

	print(f'\tCost = {cost}, Time = {ending_time_point - starting_time_point}')
	return cost