from enum import Enum
class AlgorithmsMode(Enum):
	NORMAL = 1
	BONUS_POINT = 2
	INTERMEDIATE_POINT = 3
	TELEPORT_POINT = 'advance'

INF = 1 << 31 - 1

direction = [
	[0, 1], [1, 0], [0, -1], [-1, 0]
]

def graph_size(graph):
	return len(graph), len(graph[0])

def is_in_graph(matrix, point):
	return point[0] >= 0 and point[0] < len(matrix) and point[1] >= 0 and point[1] < len(matrix[0])