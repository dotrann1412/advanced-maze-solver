from enum import Enum

class AlgorithmsMode(Enum):
	NORMAL = 0
	BONUS_POINT = 1
	INTERMEDIATE_POINT = 2
	TELEPORT_POINT = 3

direction = [
	[0, 1], [1, 0], [0, -1], [-1, 0]
]

extra_direction = [
	[0, 1], [1, 0], [0, -1], [-1, 0], 
	[-1, 1], [1, -1], [1, -1], [-1, 1]
]


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
