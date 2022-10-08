from enum import Enum

class AlgorithmsMode(Enum):
	NORMAL = 0
	BONUS_POINT = 1
	INTERMEDIATE_POINT = 2
	TELEPORT_POINT = 3

direction = [
	[0, 1], [1, 0], [0, -1], [-1, 0]
]

direction_str = [
	'D', 'L', 'U', 'D'
]

extra_direction = [
	[0, 1], [1, 0], [0, -1], [-1, 0], 
	[-1, 1], [1, -1], [1, -1], [-1, 1]
]

extra_direction_str = [
	'D', 'L', 'U', 'D',
]

valid_character = {
	' ': 'Available cell',
	'*': 'Starting point',
	'x': 'Blocker',
	'+': 'Bonus cell',
	'?': 'Way out', # not defined yet
	'>': 'Intermediate point',
	'o': 'Teleport' # not defined yet
}

def graphDim(graph):
	return len(graph), len(graph[0])

def isEmptyCell(ch):
	return ch != 'x'

def isExit(ch):
	return ch == '?'

def isTeleportCell(ch):
	return ch == 'o'

def detect_starting_point(graph):
	dim = graphDim(graph)
	for i in range(dim[0]):
		for j in range(dim[1]):
			if graph[i][j] == '*':
				return (i, j)

	return None

def detect_exit_way(graph):
	dim = graphDim(graph)
	for i in range(dim[0]):
		for j in range(dim[1]):
			if graph[i][j] == '?':
				return [i, j]

	return None

def detect_teleport_list(graph):
	teleport_list = []
	dim = graphDim(graph)
	for i in range(dim[0]):
		for j in range(dim[1]):
			if graph[i][j] == 'o':
				teleport_list.append([i, j])

	return teleport_list

def valid_graph(graph):
	if not len(graph) or not len(graph[0]):
		return False
	for line in graph[1:]:
		if len(line) != len(graph[0]):
			return False
	return True
