
from math import sqrt
from constants import *

def read_file(file_name: str = 'maze.txt'):
    
    bonus_points = []
    inter_points = []
    teleport_points = []
    matrix = None
    
    try:
        with open(file_name, 'r') as fp:
            n_bonus_points = int(fp.readline())
            for i in range(n_bonus_points):
                x, y, reward = map(int, fp.readline().split())
                bonus_points.append((x, y, reward))

            n_itermediate_points = int(fp.readline(' '))
            for i in range(n_itermediate_points):
                x, y = map(int, fp.readline().split(' '))
                inter_points.append((x, y))

            n_telepor_points = int(fp.readline(' '))
            for i in range(n_telepor_points):
                x, y, xt, yt = map(int, fp.readline().split(' '))
                teleport_points.append((x, y, xt, yt))

            matrix = [list(i) for i in fp.read().splitlines()]

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == MazeObject.START:
                    start = (i, j)

                elif matrix[i][j] == MazeObject.EMPTY:
                    if (i == 0) or (i == len(matrix)-1) or (j == 0) or (j == len(matrix[0])-1):
                        end = (i, j)

    except Exception as err:
        print('[*] Exception raised while parsing maze input file')
        print(f'\t-----> Here: {err}')
        return None, None, None, None, None, None

    return matrix, start, end, bonus_points, inter_points, teleport_points


def euclidean_distance(first_node, second_node):
    x_dif = first_node[0] - second_node[0]
    y_dif = first_node[1] - second_node[1]
    return sqrt(x_dif**2 + y_dif**2)


def manhattan_distance(first_node, second_node):
    x_dif = first_node[0] - second_node[0]
    y_dif = first_node[1] - second_node[1]
    return abs(x_dif) + abs(y_dif)


if __name__ == '__main__':
    matrix, start, end, bonus_points, inter_points, teleport_points = read_file('maze_map.txt')
    print(f'The height of the matrix: {len(matrix)}')
    print(f'The width of the matrix: {len(matrix[0])}')
    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')
