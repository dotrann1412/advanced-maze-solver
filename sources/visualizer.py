import pygame
import sys
from pygame.locals import *


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)

WIN_WIDTH = 400
WIN_HEIGHT = 300


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


def visualizer(bonus_points, matrix, start, end, block_size=20):
    global SCREEN, CLOCK
    pygame.init()
    WIN_HEIGHT = block_size * len(matrix)
    WIN_WIDTH = block_size * len(matrix[0])
    SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(PINK)
    pygame.display.set_caption('Hello World!')

    # main game loop
    while True:
        renderMap(bonus_points, matrix, start, end, block_size)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
