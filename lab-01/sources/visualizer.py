import pygame
import sys
from pygame.locals import *
from constants import *

from algorithms.algorithms_utils import AlgorithmsMode

from utils import manhattan_distance

def drawGrid(x, y, block_size=20, color=Colors.WHITE, border=Colors.WHITE):
    rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
    pygame.draw.rect(SCREEN, color, rect, block_size//2)
    pygame.draw.rect(SCREEN, border, rect, 1)

def renderMap(graph, start, end, block_size=20):
    for y in range(len(graph)):
        for x in range(len(graph[0])):
            if graph[y][x] == MazeObject.WALL:
                color = Colors.BLACK
            elif graph[y][x] == MazeObject.START:
                color = Colors.GREEN
            elif graph[y][x] == MazeObject.BONUS:
                color = Colors.BONUS_COLOR
            # add for intermediate_points, teleport_points
            # ...
            else:
                color = Colors.WHITE
            drawGrid(x, y, block_size, color)

    drawGrid(start[1], start[0], color=Colors.START_COLOR)
    drawGrid(end[1], end[0], color=Colors.END_COLOR)
    pygame.display.update()

# function to set color at cell (x, y) in grid
def set_color(x, y, color, sleep_time=30):
    drawGrid(x, y, color=color)
    pygame.display.update()
    pygame.time.wait(sleep_time)

def visualize(algorithm, graph, start, end, 
    bonus_points=[], inter_points=[], teleport_points=[], 
    block_size=20, hf=manhattan_distance
):
    global SCREEN, CLOCK
    pygame.init()
    WIN_HEIGHT = block_size * len(graph)
    WIN_WIDTH = block_size * len(graph[0])
    SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Hello World!')
    CLOCK = pygame.time.Clock()
    CLOCK.tick(60)

    # Render maze
    renderMap(graph, start, end, block_size)

    # Specify mode of graph
    mode = AlgorithmsMode.NORMAL
    if len(bonus_points) > 0:
        mode = AlgorithmsMode.BONUS_POINT
    elif len(inter_points) > 0:
        mode = AlgorithmsMode.INTERMEDIATE_POINT
    elif len(teleport_points) > 0:
        mode = AlgorithmsMode.TELEPORT_POINT

    algorithm(graph, start, end, mode, bonus_points, inter_points, teleport_points, set_color, hf=hf)

    # Wait 2 seconds before closing
    pygame.time.wait(2000)

    # while True:
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             pygame.quit()
    #             sys.exit()