import pygame
import sys
from pygame.locals import *
from constants import *

from algorithms.algorithms_utils import AlgorithmsMode
from algorithms.a_star import aStar

def drawGrid(x, y, block_size=20, color=Colors.WHITE, border=Colors.WHITE):
    rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
    pygame.draw.rect(SCREEN, color, rect, block_size//2)
    pygame.draw.rect(SCREEN, border, rect, 1)

def renderMap(bonus_points, matrix, start, end, block_size=20):
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == MazeObject.WALL:
                color = Colors.BLACK
            elif matrix[y][x] == MazeObject.START:
                color = Colors.GREEN
            elif matrix[y][x] == MazeObject.BONUS:
                color = Colors.RED
            else:
                color = Colors.WHITE
            drawGrid(x, y, block_size, color)

    drawGrid(start[1], start[0], color=Colors.ORANGE)
    drawGrid(end[1], end[0], color=Colors.BLUE)
    pygame.display.update()


# function to set color at cell (x, y) in grid
def set_color(x, y, color, sleep_time=30):
    drawGrid(x, y, color=color)
    pygame.display.update()
    # sleep_time = 10 if color == FRONTIER_COLOR else 5
    pygame.time.wait(sleep_time)

def visualizer(algorithm, matrix, start, end, bonus_points=[], inter_points=[], teleport_points=[], block_size=20):
    global SCREEN, CLOCK
    pygame.init()
    WIN_HEIGHT = block_size * len(matrix)
    WIN_WIDTH = block_size * len(matrix[0])
    SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Hello World!')
    CLOCK = pygame.time.Clock()
    CLOCK.tick(60)

    # Render maze
    renderMap(bonus_points, matrix, start, end, block_size)

    # Mode of matrix
    mode = AlgorithmsMode.NORMAL
    if len(bonus_points) > 0:
        mode = AlgorithmsMode.BONUS_POINT
    elif len(inter_points) > 0:
        mode = AlgorithmsMode.INTERMEDIATE_POINT
    elif len(teleport_points) > 0:
        mode = AlgorithmsMode.TELEPORT_POINT

    # Run algorithm
    if algorithm == Algorithms.A_STAR:
        aStar(matrix, start, end, mode, set_color)
    elif algorithm == Algorithms.BFS:
        pass
        # bfs(matrix, start, end, set_color)

    # Wait 2 seconds before closing
    # pygame.time.wait(2000)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
