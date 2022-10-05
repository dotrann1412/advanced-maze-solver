from algorithms_utils import direction, extra_direction, valid_graph, AlgorithmsMode

def __normal_dfs(graph, callback):
	dim = [len(graph), len(graph[0])]
	starting_point = __detect_starting_point(graph)
	if starting_point[0] < 0 or starting_point[0] >= dim[0] or starting_point[1] < 0 or starting_point[1] >= dim[1]:
		return None

	mark = [[False for __ in range(dim[1])] for _ in (dim[0])]
	answer = []

	def __process(current_position):
		if isExit(graph[*current_position]):
			return True

		mark[*current_position] = True

		for element in extra_direction:
			next_step = current[0] + element[0], current[1] + element[1]
			if next_step[0] < 0 or next_step[0] >= dim[0] or next_step[1] < 0 or next_step[1] >= dim[1]:
				continue

			if not mark[*next_step] and not isEmptyCell(graph[*next_step]):
				result = __process(next_step)
				if result:
					answer.append(next_step)
					return True

		mark[*current_position] = False
		return False

	mark[*starting_point] = True
	found = __process(starting_point)

	if not found:
		return None

	return answer[::-1]

def __dfs_with_bonus_point(graph, callback):
	def __process(current_position):
		pass

def __dfs_intermediate_point(graph, callback):
	def __process(current_position):
		pass

def __dfs_with_teleport_point(graph, callback):
	starting_point = __detect_starting_point(graph)
	teleport_list = teleport_list(graph)
	
	if starting_point[0] < 0 or starting_point[0] >= dim[0] or starting_point[1] < 0 or starting_point[1] >= dim[1]:
		return None

	mark = [[False for __ in range(dim[1])] for _ in (dim[0])]
	answer = []

	def __process(current_position):
		if isExit(graph[*current_position]):
			return True

		available_next_step = extra_direction

		if isTeleport(graph[*current_position]):
			available_next_step += teleport_list

		for element in available_next_step:
			next_step = current[0] + element[0], current[1] + element[1]
			if next_step[0] < 0 or next_step[0] >= dim[0] or next_step[1] < 0 or next_step[1] >= dim[1]:
				continue

			if not mark[*next_step] and not isEmptyCell(graph[*next_step]):
				
				mark[*current_position] = True
				result = __process(next_step)
				mark[*current_position] = False

				if result:
					answer.append(next_step)
					return True
		
		return False

	mark[*starting_point] = True
	found = __process(starting_point)

	if not found:
		return None

	return answer[::-1]

def dfs(graph, mode, call_back):
	if not valid_graph(graph):
		return None

	if mode == AlgorithmsMode.NORMAL:
		return __normal_dfs(graph, call_back)

	if mode == AlgorithmsMode.BONUS_POINT:
		return __dfs_with_bonus_point(graph, call_back)
	
	if mode == AlgorithmsMode.INTERMEDIATE_POINT:
		return __dfs_intermediate_point(graph, call_back)
	
	if mode == AlgorithmsMode.TELEPORT_POINT:
		return __dfs_with_teleport_point(graph, call_back)
