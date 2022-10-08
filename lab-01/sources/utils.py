from constants import *

def read_file(file_name: str = 'maze.txt'):
    f = open(file_name, 'r')
    n_bonus_points = int(next(f)[:-1])

    bonus_points = []
    inter_points = []
    teleport_points = []

    for i in range(n_bonus_points):
        x, y, reward = map(int, next(f)[:-1].split(' '))
        bonus_points.append((x, y, reward))

    text = f.read()
    matrix = [list(i) for i in text.splitlines()]
    f.close()

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == MazeObject.START:
                start = (i, j)

            elif matrix[i][j] == MazeObject.EMPTY:
                if (i == 0) or (i == len(matrix)-1) or (j == 0) or (j == len(matrix[0])-1):
                    end = (i, j)

            else:
                pass

    return matrix, start, end, bonus_points, inter_points, teleport_points


if __name__ == '__main__':
    matrix, start, end, bonus_points, inter_points, teleport_points = read_file('maze_map.txt')
    print(f'The height of the matrix: {len(matrix)}')
    print(f'The width of the matrix: {len(matrix[0])}')
    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')
