import pygame
import sys
from pygame.locals import *
from constants import *

from algorithms.bfs import bfs_testing
from algorithms.gbfs import gbfs
from utils import manhattan_distance

# for screen recorder
import cv2
from PIL import Image
import numpy as np
from datetime import datetime
import re
import os
import glob

def genFilename():
    return re.sub('[^A-Za-z0-9]+', '', str(datetime.now())) + ".png"

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
    pygame.image.save(SCREEN, 'frames/' + genFilename())


# function to set color at cell (x, y) in grid
def set_color(x, y, color, sleep_time=30):
    drawGrid(x, y, color=color)
    pygame.display.update()
    pygame.time.wait(sleep_time)
    pygame.image.save(SCREEN, 'frames/' + genFilename())

def visualizer(bonus_points, matrix, start, end, block_size=20):
    global SCREEN, CLOCK
    pygame.init()
    WIN_HEIGHT = block_size * len(matrix)
    WIN_WIDTH = block_size * len(matrix[0])
    SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption('Hello World!')

    CLOCK.tick(60)

    fps = 30
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    

    # Render maze and run algorithm
    renderMap(bonus_points, matrix, start, end, block_size)
    # result = bfs_testing(matrix, start, end, set_color)
    result = gbfs(matrix, start, end, set_color, manhattan_distance)
    # Wait 2 seconds before closing
    pygame.time.wait(2000)


    global ANIMATE 
    ANIMATE = cv2.VideoWriter('frames/demo.mp4', fourcc, fps, (WIN_WIDTH, WIN_HEIGHT))

    files = glob.glob('frames/*.png')
    for file in files:
        with Image.open(file) as data:
            frame = cv2.cvtColor(np.array(data), cv2.COLOR_BGR2RGB)
            ANIMATE.write(frame)

    ANIMATE.release()

    for file in files: 
        os.remove(file)    
    
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             pygame.quit()
    #             sys.exit()
