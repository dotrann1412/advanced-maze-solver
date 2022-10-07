import pygame
import sys
from pygame.locals import *
from constants import *

from algorithms.bfs import bfs_testing
from algorithms.gbfs import gbfs
from utils import manhattan_distance

def drawGrid(x, y, block_size=20, color=WHITE, border=WHITE):
    rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
    pygame.draw.rect(SCREEN, color, rect, block_size//2)
    pygame.draw.rect(SCREEN, border, rect, 1)

def renderMap(bonus_points, matrix, start, end, block_size=20):
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == 'x':
                color = BLACK
            elif matrix[y][x] == 'S':
                color = GREEN
            elif matrix[y][x] == '+':
                color = RED
            else:
                color = WHITE
            drawGrid(x, y, block_size, color)

    drawGrid(start[1], start[0], color=PINK)
    drawGrid(end[1], end[0], color=BLUE)
    pygame.display.update()


# function to set color at cell (x, y) in grid
def set_color(x, y, color, sleep_time=30):
    drawGrid(x, y, color=color)
    pygame.display.update()
    pygame.time.wait(sleep_time)

def visualizer(bonus_points, matrix, start, end, block_size=20):
    global SCREEN, CLOCK
    pygame.init()
    WIN_HEIGHT = block_size * len(matrix)
    WIN_WIDTH = block_size * len(matrix[0])
    SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption('Hello World!')

    CLOCK.tick(60)

    # Render maze and run algorithm
    renderMap(bonus_points, matrix, start, end, block_size)
    # result = bfs_testing(matrix, start, end, set_color)
    result = gbfs(matrix, start, end, set_color, manhattan_distance)
    # Wait 2 seconds before closing
    pygame.time.wait(2000)
    
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             pygame.quit()
    #             sys.exit()
