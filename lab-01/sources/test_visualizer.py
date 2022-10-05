from visualizer import visualizer
from utils import read_file

if __name__ == "__main__":
    bonus_points, matrix, start, end = read_file('../input-samples/maze_map.txt')
    # print(matrix)
    print(f'The height of the matrix: {len(matrix)}')
    print(f'The width of the matrix: {len(matrix[0])}')
    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')
    visualizer(bonus_points, matrix, start, end)
