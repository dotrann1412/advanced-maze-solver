from algorithms.algorithms_utils import *
from utils import manhattan_distance
from constants import *
from queue import PriorityQueue
from visualizer import set_path_color, set_frontier_color, set_color


def __normal_a_star(graph, start, end, hf, draw_path=True):
	'''
	A* algorithm for normal maze
	Heuristic function: Manhattan distance between current point and end point

	Args:
					graph: 2D array of graph
					start: starting point
					end: ending point
					hf: heuristic function
					drawPath: draw path or not (default True, we use this for other map)

	Returns:
					list of points from start to end
	'''
	def h(point):
		return hf(point, end)

	dim = [len(graph), len(graph[0])]
	sleep_time = calc_sleep_time(dim)

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
			set_frontier_color(point[1], point[0], sleep_time)

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
		set_path_color(answer, sleep_time)

	return answer


# def __a_star_with_bonus_point_recur(graph, start, end, bonus_points, hf):
# 	def h(p1, p2=end):
# 		return hf(p1, p2)

# 	def calc_h_bonus(start, point, end):
# 		'''
# 		Heuristic in a map with bonus points.
# 		'''
# 		return h(start, point) + h(point, end) + bonus_points[point]

# 	h_bonus_arr = sorted([[calc_h_bonus(start, point, end), point] for point in bonus_points])
# 	h_start = h(start)

# 	bonus_to_be_removed = []
# 	for h_bonus_item in h_bonus_arr:
# 		h_bonus, point = h_bonus_item

# 		if h_bonus >= h_start:
# 			break

# 		# go to the "best" bonus point (if possible)
# 		part1 = __normal_a_star(graph, start, point, hf, draw_path=False)
# 		if part1 is None:
# 			bonus_to_be_removed.append(point)
# 			continue

# 		# remove bonus point that we don't need to consider in part2
# 		next_bonus_points = bonus_points.copy()
# 		next_bonus_points.pop(point)
# 		for cant_reach_point in bonus_to_be_removed:    # start can't go to these bonus points
# 			next_bonus_points.pop(cant_reach_point)
# 		for reached_point in part1:     # we already go through these bonus points in part1
# 			if reached_point in next_bonus_points:
# 				next_bonus_points.pop(reached_point)

# 		# go from the "best" bonus point to end
# 		part2 = __a_star_with_bonus_point_recur(graph, point, end, next_bonus_points, hf)
# 		if part2 is None:
# 			continue

# 		return part1[:-1] + part2

# 	# if we can't go to any bonus point to get profit, just go to end directly
# 	return __normal_a_star(graph, start, end, hf, draw_path=False)

# def __a_star_with_bonus_point(graph, start, end, bonus_points, hf):
# 	dim = [len(graph), len(graph[0])]
# 	sleep_time = calc_sleep_time(dim)

# 	# answer = []

# 	answer = __a_star_with_bonus_point_recur(graph, start, end, bonus_points, hf)

# 	# bonus_dict = {}
# 	# for bonus in bonus_points:
# 	# 	bonus_dict[bonus[:2]] = [bonus[2], False]   # [value of bonus, is visited]

# 	bonus_points_cp = bonus_points.copy()
# 	cost = len(answer) - 1
# 	for point in answer:
# 		if point in bonus_points_cp:
# 			cost += bonus_points_cp[point]
# 			bonus_points_cp[point] = 0

# 	# reset color of start and end
# 	set_color(start[1], start[0], color=Colors.START, sleep_time=0)
# 	set_color(end[1], end[0], color=Colors.END, sleep_time=0)

# 	# draw bonus points again
# 	for point in bonus_points:
# 		set_color(point[1], point[0], Colors.SPECIAL, 0)

# 	set_path_color(answer, sleep_time, bonus_points)

# 	print(answer)
# 	print(cost)
# 	return answer, cost

def __a_star_with_bonus_point(graph, start, end, bonus_points, hf, run_for_inter=False):
	dim = [len(graph), len(graph[0])]
	sleep_time = calc_sleep_time(dim)

	special_points = [end] + list(bonus_points.keys())

	bonus_points_cp = bonus_points.copy()

	def extra_hf(point):
		val = INF
		for p in special_points:
			cur_h_val = (3 if run_for_inter else 1) * hf(point, p) + hf(p, end) + \
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
			if run_for_inter == False or len(bonus_points_cp) == 0:
				found = True
				break
			else:
				continue

		if point != start:
			set_frontier_color(point[1], point[0], sleep_time)

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
					print('[DEBUG] reach bonus', child)
					path_to_bonus[child] = __trace_back_bonus(child)

	if not found:
		print('[DEBUG] not found')
		return None

	answer = []

	cost = g[end[0]][end[1]]
	answer = __trace_back_bonus(end)
	magican = answer[0]

	while magican != start:
		answer = path_to_bonus[magican] + answer[1:]
		magican = answer[0]

	if run_for_inter == False:
		for bonus in bonus_points:
			set_color(bonus[1], bonus[0], Colors.SPECIAL, 0)

		set_path_color(answer, sleep_time, bonus_points)
	
	print(answer)
	print('Cost: ', cost)
	return answer, cost


def __a_star_intermediate_point(graph, start, end, intermediate_points, hf):
	dim = [len(graph), len(graph[0])]
	sleep_time = calc_sleep_time(dim)

	bonus_points = {}
	for point in intermediate_points:
		bonus_points[point] = -INF

	answer, _ = __a_star_with_bonus_point(
		graph, start, end, bonus_points, hf, run_for_inter=True)

	for point in intermediate_points:
		if point not in answer:
			print('[DEBUG] not found')
			return None

	for bonus in bonus_points:
		set_color(bonus[1], bonus[0], Colors.SPECIAL, 0)

	set_path_color(answer, sleep_time, bonus_points)

	print(answer)
	print(len(answer) - 1)

	return answer


def __a_star_with_teleport_point(graph, start, end, teleport_points, hf):
	def h(point):
		return hf(point, end)

	dim = [len(graph), len(graph[0])]
	sleep_time = calc_sleep_time(dim)

	special_points = [end] + list(teleport_points.keys())

	def __extra_heuristic(point):
		val = INF
		for p in special_points:
			val = min(val, hf(p, end) + hf(point, p))
			if p in teleport_points:
				val = min(val, hf(teleport_points[p], end), hf(point, p))
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
			set_frontier_color(point[1], point[0], sleep_time)

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
	set_path_color(answer, sleep_time, special_points)

	return answer


def a_star(graph, start, end, mode, bonus_points, intermediate_points, teleport_points, hf=manhattan_distance):
	if not is_valid_graph(graph):
		return None

	if mode == AlgorithmsMode.NORMAL:
		return __normal_a_star(graph, start, end, hf)

	if mode == AlgorithmsMode.BONUS_POINT:
		return __a_star_with_bonus_point(graph, start, end, bonus_points, hf)

	if mode == AlgorithmsMode.INTERMEDIATE_POINT:
		return __a_star_intermediate_point(graph, start, end, intermediate_points, hf)

	if mode == AlgorithmsMode.TELEPORT_POINT:
		return __a_star_with_teleport_point(graph, start, end, teleport_points, hf)
