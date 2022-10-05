from algorithms_utils import direction, valid_graph, AlgorithmsMode

def __detect_starting_point(graph):
	pass

def __normal_bfs(graph):
	dim = [len(graph), len(graph[0])]
	queue = []
	starting_point = __detect_starting_point(graph)
	parrent = [[for __ in range(dim[1])] for _ in (dim[0])]
	queue.append(starting_point)
	


def __bfs_with_bonus_point(graph):
	starting_point = __detect_starting_point(graph)

def __bfs_intermediate_point(graph):
	starting_point = __detect_starting_point(graph)

def __bfs_with_teleport_point(graph):
	starting_point = __detect_starting_point(graph)

def bfs(graph, mode):
	if not valid_graph(graph):
		return None

	if mode == AlgorithmsMode.NORMAL:
		return __normal_bfs(graph)

	if mode == AlgorithmsMode.BONUS_POINT:
		return __bfs_with_bonus_point(graph)
	
	if mode == AlgorithmsMode.INTERMEDIATE_POINT:
		return __bfs_intermediate_point(graph)
	
	if mode == AlgorithmsMode.TELEPORT_POINT:
		return __bfs_with_teleport_point(graph)

