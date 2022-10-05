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

def isEmptyCell(ch):
	pass

def isExit(ch):
	pass

def isTeleportCell(char):
	pass

def detect_starting_point(graph):
	pass

def detect_exit_way(graph):
	pass

def teleport_list(graph):
	pass



valid_character = {
	' ': 'Available cell',
	'*': 'Starting point',
	'x': 'Blocker',
	'+': 'Bonus cell',
	'?': 'Way out' # not defined yet
	'?': 'Intermediate point'
	'??': 'Teleport' # not defined yet
}

def valid_graph(graph):
	if not len(graph) or not len(graph[0]):
		return False
	for line in graph[1:]:
		if len(line) != len(graph[0]):
			return False
	return True
