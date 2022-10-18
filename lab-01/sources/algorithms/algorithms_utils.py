from enum import Enum
class AlgorithmsMode(Enum):
	NORMAL = 0
	BONUS_POINT = 1
	INTERMEDIATE_POINT = 2
	TELEPORT_POINT = 3

INF = 1 << 31 - 1

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
	'o': 'Teleport' # not defined yet
}

def graph_size(graph):
	return len(graph), len(graph[0])

def is_empty_cell(ch):
	return ch != 'x'

def is_exit(ch):
	return ch == '?'

def is_teleport_cell(ch):
	return ch == 'o'

def detect_starting_point(graph):
	dim = graph_size(graph)
	for i in range(dim[0]):
		for j in range(dim[1]):
			if graph[i][j] == '*':
				return (i, j)

	return None

def detect_ending_point(graph):
	dim = graph_size(graph)
	for i in range(dim[0]):
		for j in range(dim[1]):
			if graph[i][j] == '?':
				return [i, j]

	return None

def detect_teleport_list(graph):
	teleport_list = []
	dim = graph_size(graph)
	for i in range(dim[0]):
		for j in range(dim[1]):
			if graph[i][j] == 'o':
				teleport_list.append([i, j])

	return teleport_list

def is_valid_graph(graph):
	if not len(graph) or not len(graph[0]):
		return False
	for line in graph[1:]:
		if len(line) != len(graph[0]):
			return False
	return True

def is_in_graph(matrix, point):
	return point[0] >= 0 and point[0] < len(matrix) and point[1] >= 0 and point[1] < len(matrix[0])

def calc_sleep_time(dim):
	return min(max(15000 // dim[0] // dim[1], 15), 30)
