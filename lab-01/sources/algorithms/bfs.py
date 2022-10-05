from algorithms_utils import direction, extra_direction, valid_graph, AlgorithmsMode

def __normal_bfs(graph, callback):
	dim = [len(graph), len(graph[0])]
	queue = []
	starting_point = __detect_starting_point(graph)

	if starting_point[0] < 0 or starting_point[0] >= dim[0] or starting_point[1] < 0 or starting_point[1] >= dim[1]:
		return None

	parrent = [[None for __ in range(dim[1])] for _ in (dim[0])]
	
	queue.append(starting_point)
	parrent[*starting_point] = starting_point
	
	found = False

	while len(queue) != 0 and not found:
		current = queue[0]
		queue.pop(0)
		for element in extra_direction:
			next_step = current[0] + element[0], current[1] + element[1]
			
			if next_step[0] < 0 or next_step[0] >= dim[0] or next_step[1] < 0 or next_step[1] >= dim[1]:
				continue

			if isExit(graph[*next_step]):
				parrent[*next_step] = current
				found = True
				break

			if isEmptyCell(graph[*next_step]) and not parrent[*next_step]:
				parrent[*next_step] = current
				queue.append(next_step)

	wayout_position = __detect_exit_way(graph)

	if not wayout_position or not parrent[*wayout_position]:
		return None

	answer = []
	pointer = wayout_position

	while parrent[*pointer] != starting_point:
		answer.append(pointer)
		pointer = parrent[*pointer]

	return answer[::-1]

def __bfs_with_bonus_point(graph, callback):
	dim = [len(graph), len(graph[0])]
	starting_point = __detect_starting_point(graph)

def __bfs_intermediate_point(graph, callback):
	starting_point = __detect_starting_point(graph)

def __bfs_with_teleport_point(graph, callback):
	starting_point = __detect_starting_point(graph)
	queue = []

	teleport_list = teleport_list(graph)
	is_used_teleport = False

	if starting_point[0] < 0 or starting_point[0] >= dim[0] or starting_point[1] < 0 or starting_point[1] >= dim[1]:
		return None

	parrent = [[None for __ in range(dim[1])] for _ in (dim[0])]
	
	if isTeleport(graph[*starting_point]):
		for teleport in teleport_list:
			parrent[*teleport] = starting_point
			queue.append(teleport)
		is_used_teleport = True
	else:
		queue.append(starting_point)
		parrent[*starting_point] = starting_point

	found = False

	while len(queue) != 0 and not found:
		current = queue[0]
		queue.pop(0)

		for element in extra_direction:
			next_step = current[0] + element[0], current[1] + element[1]
			if next_step[0] < 0 or next_step[0] >= dim[0] or next_step[1] < 0 or next_step[1] >= dim[1]:
				continue

			if isExit(graph[*next_step]):
				parrent[*next_step] = current
				found = True
				break

			if isTeleport(*next_step) and not is_used_teleport:
				for teleport in teleport_list:
					parrent[*teleport] = starting_point if teleport != next_step else current
					queue.append(teleport)
				is_used_teleport = True
				continue

			if isEmptyCell(graph[*next_step]) and not parrent[*next_step]:
				parrent[*next_step] = current
				queue.append(next_step)


	wayout_position = __detect_exit_way(graph)

	if not wayout_position or not parrent[*wayout_position]:
		return None

	answer = []
	pointer = wayout_position

	while parrent[*pointer] != starting_point:
		answer.append(pointer)
		pointer = parrent[*pointer]

	return answer[::-1]


def bfs(graph, mode, call_back):
	if not valid_graph(graph):
		return None

	if mode == AlgorithmsMode.NORMAL:
		return __normal_bfs(graph, call_back)

	if mode == AlgorithmsMode.BONUS_POINT:
		return __bfs_with_bonus_point(graph, call_back)
	
	if mode == AlgorithmsMode.INTERMEDIATE_POINT:
		return __bfs_intermediate_point(graph, call_back)
	
	if mode == AlgorithmsMode.TELEPORT_POINT:
		return __bfs_with_teleport_point(graph, call_back)

