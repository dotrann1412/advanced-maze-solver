import pygame
import sys
from pygame.locals import *
from constants import *

from utils import manhattan_distance, darker_color

# for screen recorder
import cv2
from PIL import Image
import numpy as np


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
				color = Colors.SPECIAL
			# add for intermediate_points, teleport_points
			# ...
			else:
				color = Colors.WHITE
			drawGrid(x, y, block_size, color)

	drawGrid(start[1], start[0], color=Colors.START)
	drawGrid(end[1], end[0], color=Colors.END)
	pygame.display.update()

	# write frame to MP4 output
	if ANIMATE is not None:
		current_frame_str = pygame.image.tostring(SCREEN, "RGB")
		current_frame_dat = Image.frombytes(
			'RGB', (WIN_WIDTH, WIN_HEIGHT), bytes(current_frame_str), 'raw')
		frame = cv2.cvtColor(np.array(current_frame_dat), cv2.COLOR_BGR2RGB)
		ANIMATE.write(frame)


def get_color(x, y, block_size=20,):
	global SCREEN
	return SCREEN.get_at((x * block_size + block_size // 2, y * block_size + block_size // 2))

# function to set color at cell (x, y) in grid


def set_color(x, y, color, sleep_time=30):
	drawGrid(x, y, color=color)
	pygame.display.update()
	pygame.time.wait(sleep_time)

	# write frame to MP4 output
	if ANIMATE is not None:
		current_frame_str = pygame.image.tostring(SCREEN, "RGB")
		current_frame_dat = Image.frombytes(
			'RGB', (WIN_WIDTH, WIN_HEIGHT), bytes(current_frame_str), 'raw')
		frame = cv2.cvtColor(np.array(current_frame_dat), cv2.COLOR_BGR2RGB)
		ANIMATE.write(frame)


def set_frontier_color(x, y, sleep_time):
	color = Colors.FRONTIER
	cur_color = get_color(x, y)
	if cur_color != Colors.WHITE:
		color = darker_color(cur_color)
	set_color(x, y, color, sleep_time)


def set_path_color(path, sleep_time, special_points={}):
	passed = {}
	for point in path:
		passed[point] = False

	for point in path:
		color = Colors.PATH
		cur_color = get_color(point[1], point[0])
		if cur_color == Colors.PATH or cur_color == Colors.SPECIAL or point in special_points or passed[point]:
			color = darker_color(cur_color)
		passed[point] = True
		set_color(point[1], point[0], color, sleep_time)


def visualize(algorithm, mode, graph, start, end,
			  bonus_points=[], inter_points=[], teleport_points=[],
			  block_size=20, hf=manhattan_distance,
			  output_path=None
			  ):
	global SCREEN, CLOCK
	pygame.init()
	global WIN_WIDTH, WIN_HEIGHT
	WIN_HEIGHT = block_size * len(graph)
	WIN_WIDTH = block_size * len(graph[0])
	SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	pygame.display.set_caption('Hello World!')
	CLOCK = pygame.time.Clock()
	CLOCK.tick(60)

	fps = 30
	fourcc = cv2.VideoWriter_fourcc(*"mp4v")
	global ANIMATE
	if output_path is not None:
		ANIMATE = cv2.VideoWriter(
			output_path, fourcc, fps, (WIN_WIDTH, WIN_HEIGHT))
	else:
		ANIMATE = None

	# Render maze
	renderMap(graph, start, end, block_size)

	algorithm(graph, start, end, mode, bonus_points,
			  inter_points, teleport_points, hf=hf)
	if ANIMATE is not None:
		ANIMATE.release()
		print('released')

	# Wait 2 seconds before closing
	pygame.time.wait(1000)
