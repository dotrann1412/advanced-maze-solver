from enum import Enum
class AlgorithmsMode(Enum):
	NORMAL = 0
	BONUS = 1
	INTERMEDIATE = 2
	TELEPORT = 3

INF = 1 << 31 - 1

direction = [
	[0, 1], [1, 0], [0, -1], [-1, 0]
]

def graph_size(graph):
	return len(graph), len(graph[0])

def is_in_graph(matrix, point):
	return point[0] >= 0 and point[0] < len(matrix) and point[1] >= 0 and point[1] < len(matrix[0])