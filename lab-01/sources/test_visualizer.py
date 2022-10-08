from constants import *
from visualizer import visualizer
from utils import read_file

if __name__ == "__main__":
    matrix, start, end, bonus_points, inter_points, teleport_points = read_file('../input-samples/maze_map.txt')

    print(f'The height of the matrix: {len(matrix)}')
    print(f'The width of the matrix: {len(matrix[0])}')
    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')

    # visualizer(BFS, matrix, start, end, bonus_points, inter_points, teleport_points)
    visualizer(Algorithms.A_STAR, matrix, start, end, bonus_points, inter_points, teleport_points)
