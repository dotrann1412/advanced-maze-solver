from algorithms.algorithms_utils import *
from utils import manhattan_distance
from constants import *
from queue import PriorityQueue
from visualizer import set_path_color, set_frontier_color, set_color

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
def __normalAStar(graph, start, end, hf, drawPath=True):
	def h(point):
		return hf(point, end)

	dim = [len(graph), len(graph[0])]
	sleep_time = calcSleepTime(dim)

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
			if not isInGraph(graph, child) or graph[child[0]][child[1]] == MazeObject.WALL:
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

	if drawPath:
		set_path_color(answer, sleep_time)
		
	return answer


def __aStarWithBonusPointRecur(graph, start, end, bonus_points, hf):
	def h(p1, p2=end):
		return hf(p1, p2)

	def calcHBonus(start, bonus, end):
		return 3 * h(start, bonus[:2]) + +  h(bonus[:2], end) + bonus[2]

	hBonusArr = sorted([[calcHBonus(start, bonus, end), bonus] for bonus in bonus_points])
	hStart = h(start)

	bonus_to_be_removed = []
	for hBonusItem in hBonusArr:
		hBonus, bonus = hBonusItem
		
		if hBonus >= hStart:
			break

		# go to the "best" bonus point (if possible)
		part1 = __normalAStar(graph, start, bonus[:2], hf, drawPath=False)
		if part1 is None:
			bonus_to_be_removed.append(bonus)
			continue
		
		# remove bonus point that we don't need to consider in part2
		next_bonus_points = bonus_points.copy()
		next_bonus_points.remove(bonus)
		for cant_reach_point in bonus_to_be_removed:    # start can't go to these bonus points
			next_bonus_points.remove(cant_reach_point) 
		for reached_point in part1:     # we already go through these bonus points in part1
			for bonus_point in next_bonus_points:
				if reached_point == bonus_point[:2]:
					next_bonus_points.remove(bonus_point)
			
		# go from the "best" bonus point to end
		part2 = __aStarWithBonusPointRecur(graph, bonus[:2], end, next_bonus_points, hf)
		if part2 is None:
			continue

		return part1[:-1] + part2
	
	# if we can't go to any bonus point to get profit, just go to end directly
	return __normalAStar(graph, start, end, hf, drawPath=False)

def __aStarWithBonusPoint(graph, start, end, bonus_points, hf):
	dim = [len(graph), len(graph[0])]
	sleep_time = calcSleepTime(dim)

	answer = []

	# answer = __aStarWithBonusPointRecur(graph, start, end, bonus_points, hf)

	bonus_dict = {}
	for bonus in bonus_points:
		bonus_dict[bonus[:2]] = [bonus[2], False]   # [value of bonus, is visited]
	
	cost = len(answer) - 1
	for point in answer:
		if point in bonus_dict:
			cost += bonus_dict[point][0]
			bonus_dict[point][0] = 0
			bonus_dict[point][1] = True    

	# reset color of start and end
	set_color(start[1], start[0], color=Colors.START_COLOR, sleep_time=0)
	set_color(end[1], end[0], color=Colors.END_COLOR, sleep_time=0)

	# draw bonus points again
	for bonus in bonus_dict:
		set_color(bonus[1], bonus[0], Colors.BONUS_COLOR, 100)

	set_path_color(answer, sleep_time)
	
	print(answer)
	print(cost)
	return answer, cost
		

def __aStarIntermediatePoint(graph, start, end, intermediate_points, hf):
	bonus_points = []
	for point in intermediate_points:
		bonus_points.append([point[0], point[1], -INF])
	
	answer, cost = __aStarWithBonusPoint(graph, start, end, bonus_points, hf)
	for point in intermediate_points:
		if point not in answer:
			return None
	
	return answer

def __aStarWithTeleportPoint(graph, start, end, teleport_points, hf):
	def h(point):
		return hf(point, end)

	dim = [len(graph), len(graph[0])]
	sleep_time = calcSleepTime(dim)

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
			if not isInGraph(graph, child) or graph[child[0]][child[1]] == MazeObject.WALL:
				continue

			if g[child[0]][child[1]] > g[point[0]][point[1]] + 1:
				g[child[0]][child[1]] = g[point[0]][point[1]] + 1
				parent[child[0]][child[1]] = point
				pq.put([g[child[0]][child[1]] + h(child), h(child), child])

			if (child[0], child[1]) in teleport_points:
				dest_x, dest_y = teleport_points[(child[0], child[1])]
				if g[dest_x, dest_y] > g[point[0]][point[1]] + 1:
					g[dest_x, dest_y] = g[point[0]][point[1]] + 1
					parent[dest_x, dest_y] = point
					pq.put([g[dest_x, dest_y] + h((dest_x, dest_y)), h((dest_x, dest_y)), (dest_x, dest_y)])
		
	if not found:
		return None
	
	answer = []
	pointer = end

	while pointer != start:
		answer.append(pointer)
		pointer = parent[pointer[0]][pointer[1]]
	answer.append(start)
	answer = answer[::-1]

	set_path_color(answer, sleep_time)
	
	return answer


def aStar(graph, start, end, mode, bonus_points, intermediate_points, teleport_points, hf=manhattan_distance):
	if not isValidGraph(graph):
		return None

	if mode == AlgorithmsMode.NORMAL:
		return __normalAStar(graph, start, end, hf)

	if mode == AlgorithmsMode.BONUS_POINT:
		return __aStarWithBonusPoint(graph, start, end, bonus_points, hf)

	if mode == AlgorithmsMode.INTERMEDIATE_POINT:
		return __aStarIntermediatePoint(graph, start, end, intermediate_points, hf)

	if mode == AlgorithmsMode.TELEPORT_POINT:
		return __aStarWithTeleportPoint(graph, start, end, teleport_points, hf)
