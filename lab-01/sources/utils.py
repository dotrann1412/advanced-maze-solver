
from enum import Enum
from math import sqrt
from constants import *
from algorithms.algorithms_utils import AlgorithmsMode
import os

def read_file(file_name: str = 'maze.txt', mode: Enum = AlgorithmsMode.NORMAL) -> list:
    bonus_points = {}
    inter_points = []
    teleport_points = {}
    graph = None
    start, end = (-1, -1), (-1, -1)

    try:
        with open(file_name, 'r') as fp:
            n_special_points = int(fp.readline())

            for i in range(n_special_points):
                if mode == AlgorithmsMode.BONUS_POINT:
                    x, y, reward = map(int, fp.readline().split())
                    bonus_points[(x, y)] = reward
                elif mode == AlgorithmsMode.INTERMEDIATE_POINT:
                    x, y = map(int, fp.readline().split())
                    inter_points.append((x, y))
                elif mode == AlgorithmsMode.TELEPORT_POINT:
                    x1, y1, x2, y2 = map(int, fp.readline().split())
                    teleport_points[(x1, y1)] = (x2, y2)
                    teleport_points[(x2, y2)] = (x1, y1)

            text = fp.read()
            graph = [list(i) for i in text.splitlines()]

        for i in range(len(graph)):
            for j in range(len(graph[0])):
                if graph[i][j] == MazeObject.START:
                    start = (i, j)

                elif graph[i][j] == MazeObject.EMPTY:
                    if (i == 0) or (i == len(graph)-1) or (j == 0) or (j == len(graph[0])-1):
                        end = (i, j)

    except Exception as err:
        print('[*] Exception raised while parsing maze input file')
        print(f'\t-----> Here: {err}')
        return None, None, None, None, None, None

    return graph, start, end, bonus_points, inter_points, teleport_points

def euclidean_distance(first_node, second_node):
    dx = first_node[0] - second_node[0]
    dy = first_node[1] - second_node[1]
    return sqrt(dx**2 + dy**2)


def manhattan_distance(first_node, second_node):
    dx = first_node[0] - second_node[0]
    dy = first_node[1] - second_node[1]
    return abs(dx) + abs(dy)

def darker_color(color, factor=60):
    # set the color to a darker shade
    color = [max(0, i - factor) for i in color]
    return tuple(color)

def mkdir_plus(dir):
    dir = dir.replace('\\', '/').split('/')
    tmp = ''
    for d in dir:
        tmp = os.path.join(tmp, d)
        if not os.path.exists(tmp):
            os.mkdir(tmp)