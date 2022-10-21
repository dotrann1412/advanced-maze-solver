from algorithms.algorithms_utils import *
from utils import manhattan_distance
from constants import *
from queue import PriorityQueue
from visualizer import set_path_color, set_frontier_color, set_color
from datetime import datetime


def __normal_a_star(graph, start, end, hf, draw_path=True):
	def h(point):
		return hf(point, end)

	dim = [len(graph), len(graph[0])]

	parent = [[None for __ in range(dim[1])] for _ in range(dim[0])]
	g = [[float('inf') for __ in range(dim[1])] for _ in range(dim[0])]
	g[start[0]][start[1]] = 0

	pq = PriorityQueue()
	# pq compare f, then h (if f of two node are equal)
	pq.put([g[start[0]][start[1]] + h(start), h(start), start])

	found = False
	while not pq.empty():
		_, _, point = pq.get()

		if point == end:
			found = True
			break

		if point != start:
			set_frontier_color(point[1], point[0])

		for d in direction:
			child = (point[0] + d[0], point[1] + d[1])
			if not is_in_graph(graph, child) or graph[child[0]][child[1]] == MazeObject.WALL:
				continue

			if g[child[0]][child[1]] > g[point[0]][point[1]] + 1:
				g[child[0]][child[1]] = g[point[0]][point[1]] + 1
				parent[child[0]][child[1]] = point
				pq.put([g[child[0]][child[1]] + h(child), h(child), child])

	if not found:
		return None

	answer = []
	pointer = end

	while pointer != start:
		answer.append(pointer)
		pointer = parent[pointer[0]][pointer[1]]
	answer.append(start)

	answer = answer[::-1]

	if draw_path:
		set_path_color(answer)

	return len(answer) - 1


def __a_star_with_bonus_point(graph, start, end, bonus_points, hf):
	dim = [len(graph), len(graph[0])]

	special_points = [end] + list(bonus_points.keys())

	bonus_points_cp = bonus_points.copy()

	def extra_hf(point):
		val = INF
		for p in special_points:
			cur_h_val = hf(point, p) + hf(p, end) + \
				(bonus_points_cp[p] if p in bonus_points_cp else 0)
			val = min(val, cur_h_val)
		return val

	path_to_bonus = {}
	parent = [[None for __ in range(dim[1])] for _ in range(dim[0])]
	g = [[float('inf') for __ in range(dim[1])] for _ in range(dim[0])]
	g[start[0]][start[1]] = 0

	def __trace_back_bonus(point):
		pointer = point
		path = [point]
		while True:
			pointer = parent[pointer[0]][pointer[1]]
			path.append(pointer)
			check = True

			for d in direction:
				par_next_x, par_next_y = pointer[0] + d[0], pointer[1] + d[1]
				if g[par_next_x][par_next_y] < g[pointer[0]][pointer[1]]:
					check = False
					break

			if check:
				break

		return path[::-1]

	frontier = PriorityQueue()
	# pq compare f, then h (if f of two node are equal)
	frontier.put([g[start[0]][start[1]] +
				 extra_hf(start), extra_hf(start), start])

	found = False
	while not frontier.empty():
		_, _, point = frontier.get()

		if point == end:
			found = True
			break

		if point != start:
			set_frontier_color(point[1], point[0])

		for d in direction:
			child = (point[0] + d[0], point[1] + d[1])
			if not is_in_graph(graph, child) or graph[child[0]][child[1]] == MazeObject.WALL:
				continue

			bonus = bonus_points_cp.pop(child, 0)
			new_g = g[point[0]][point[1]] + 1 + bonus

			if new_g < g[child[0]][child[1]]:
				parent[child[0]][child[1]] = point
				g[child[0]][child[1]] = new_g

				frontier.put([g[child[0]][child[1]] +
							 extra_hf(child), extra_hf(child), child])
 
				if bonus != 0:
					path_to_bonus[child] = __trace_back_bonus(child)

	if not found:
		return None

	answer = []

	cost = g[end[0]][end[1]]
	answer = __trace_back_bonus(end)
	magican = answer[0]

	while magican != start:
		answer = path_to_bonus[magican] + answer[1:]
		magican = answer[0]

	for bonus in bonus_points:
		set_color(bonus[1], bonus[0], Colors.SPECIAL, 0)

	set_path_color(answer, bonus_points)
	
	return cost


def __a_star_intermediate_point(graph, start, end, intermediate_points, hf):
	dim = [len(graph), len(graph[0])]

	intermediate_points_cp = intermediate_points.copy()
	for point in intermediate_points_cp:
		intermediate_points_cp[point] = -INF

	def extra_hf(point):
		if len(intermediate_points_cp) == 0:
			return hf(point, end)

		val = INF
		for p in intermediate_points_cp:
			cur_h_val = hf(point, p)
			val = min(val, cur_h_val)
		return val

	path_to_bonus = {}
	parent = [[None for __ in range(dim[1])] for _ in range(dim[0])]
	g = [[float('inf') for __ in range(dim[1])] for _ in range(dim[0])]
	g[start[0]][start[1]] = 0

	def __trace_back(point):
		pointer = point
		path = [point]
		while True:
			pointer = parent[pointer[0]][pointer[1]]
			path.append(pointer)
			check = True

			for d in direction:
				par_next_x, par_next_y = pointer[0] + d[0], pointer[1] + d[1]
				if g[par_next_x][par_next_y] < g[pointer[0]][pointer[1]]:
					check = False
					break

			if check:
				break

		return path[::-1]

	frontier = PriorityQueue()
	# pq compare f, then h (if f of two node are equal)
	frontier.put([g[start[0]][start[1]] +
				 extra_hf(start), extra_hf(start), start])

	found = False
	while not frontier.empty():
		_, _, point = frontier.get()

		if point == end:
			if len(intermediate_points_cp) == 0:
				found = True
				break
			else:
				continue

		if point != start:
			set_frontier_color(point[1], point[0])

		for d in direction:
			child = (point[0] + d[0], point[1] + d[1])
			if not is_in_graph(graph, child) or graph[child[0]][child[1]] == MazeObject.WALL:
				continue

			bonus = intermediate_points_cp.pop(child, 0)
			new_g = g[point[0]][point[1]] + 1 + bonus
			
			if new_g < g[child[0]][child[1]]:
				parent[child[0]][child[1]] = point
				g[child[0]][child[1]] = new_g

				frontier.put([g[child[0]][child[1]] +
							 extra_hf(child), extra_hf(child), child])

				if bonus != 0:
					path_to_bonus[child] = __trace_back(child)

	if not found:
		return None

	answer = []

	answer = __trace_back(end)
	magican = answer[0]

	while magican != start:
		answer = path_to_bonus[magican] + answer[1:]
		magican = answer[0]

	for point in intermediate_points:
		set_color(point[1], point[0], Colors.SPECIAL, 0)

	set_path_color(answer, intermediate_points)
	
	return len(answer) - 1


def __a_star_with_teleport_point(graph, start, end, teleport_points, hf):
	def h(point):
		return hf(point, end)

	dim = [len(graph), len(graph[0])]

	special_points = [end] + list(teleport_points.keys())

	def __extra_heuristic(point):
		val = INF
		for p in special_points:
			val = min(val, hf(p, end) + hf(point, p))
			if p in teleport_points:
				val = min(val, hf(teleport_points[p], end) + hf(point, p))
		return val

	def h(point):
		return __extra_heuristic(point)

	parent = [[None for __ in range(dim[1])] for _ in range(dim[0])]
	g = [[float('inf') for __ in range(dim[1])] for _ in range(dim[0])]
	g[start[0]][start[1]] = 0

	pq = PriorityQueue()
	# pq compare f, then h (if f of two node are equal)
	pq.put([g[start[0]][start[1]] + h(start), h(start), start])

	found = False
	while not pq.empty():
		_, _, point = pq.get()

		if point == end:
			found = True
			break

		if point != start:
			set_frontier_color(point[1], point[0])

		for d in direction:
			child = (point[0] + d[0], point[1] + d[1])
			if not is_in_graph(graph, child) or graph[child[0]][child[1]] == MazeObject.WALL:
				continue

			if g[child[0]][child[1]] > g[point[0]][point[1]] + 1:
				g[child[0]][child[1]] = g[point[0]][point[1]] + 1
				parent[child[0]][child[1]] = point
				pq.put([g[child[0]][child[1]] + h(child), h(child), child])

			if (child[0], child[1]) in teleport_points:
				dest_x, dest_y = teleport_points[(child[0], child[1])]
				if g[dest_x][dest_y] > g[point[0]][point[1]] + 1:
					g[dest_x][dest_y] = g[point[0]][point[1]] + 1
					parent[dest_x][dest_y] = point
					pq.put([g[dest_x][dest_y] + h((dest_x, dest_y)), h((dest_x, dest_y)), (dest_x, dest_y)])
		
	if not found:
		return None

	answer = []
	pointer = end

	while pointer != start:
		answer.append(pointer)
		pointer = parent[pointer[0]][pointer[1]]
	answer.append(start)
	answer = answer[::-1]

	special_points = {}
	for teleport_point in teleport_points:
		special_points[teleport_point] = True
		special_points[teleport_points[teleport_point]] = True
	set_path_color(answer, special_points)

	return len(answer) - 1

def a_star(graph, start, end, mode, bonus_points, intermediate_points, teleport_points, hf=manhattan_distance):
	if mode == AlgorithmsMode.NORMAL:
		starting_time_point = datetime.now()
		cost = __normal_a_star(graph, start, end, hf)
		ending_time_point = datetime.now()
		print('[*][A_STAR] Normal mode')
	
	elif mode == AlgorithmsMode.BONUS:
		starting_time_point = datetime.now()
		cost = __a_star_with_bonus_point(graph, start, end, bonus_points, hf)
		ending_time_point = datetime.now()
		print('[*][A_STAR] Bonus mode')

	elif mode == AlgorithmsMode.INTERMEDIATE:
		starting_time_point = datetime.now()
		cost = __a_star_intermediate_point(graph, start, end, intermediate_points, hf)
		ending_time_point = datetime.now()
		print('[*][A_STAR] Intermediate mode')

	elif mode == AlgorithmsMode.TELEPORT:
		starting_time_point = datetime.now()
		cost = __a_star_with_teleport_point(graph, start, end, teleport_points, hf)
		ending_time_point = datetime.now()
		print('[*][A_STAR] Teleport mode')
	
	else:
		print('[*][A_STAR] Unknown mode')
		return None

	print(f'\tCost = {cost}, Time = {ending_time_point - starting_time_point}')
	return cost