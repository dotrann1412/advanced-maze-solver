import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from pygame.locals import *
from constants import *

from utils import manhattan_distance, darker_color

# for screen recorder
import cv2
from PIL import Image
import numpy as np



def draw_grid(x, y, color=Colors.WHITE, block_size=Grid.BLOCK_SIZE, border=Colors.WHITE):
	rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
	pygame.draw.rect(SCREEN, color, rect, block_size // 2)
	pygame.draw.rect(SCREEN, border, rect, 1)

def write_text(text, x, y, color, block_size=Grid.BLOCK_SIZE, font_size=Grid.FONT_SIZE):
	font = pygame.font.SysFont('Comic Sans MS', font_size)
	content = font.render(text, True, color)
	SCREEN.blit(content,
				(x * block_size + block_size // 2 - len(text) * font_size // 4,
				y * block_size + block_size // 5))
	pygame.display.update()
	write_frame()


# write frame to MP4 output
def write_frame():
	if ANIMATE is not None:
		current_frame_str = pygame.image.tostring(SCREEN, "RGB")
		current_frame_dat = Image.frombytes(
			'RGB', (WIN_WIDTH, WIN_HEIGHT), bytes(current_frame_str), 'raw')
		frame = cv2.cvtColor(np.array(current_frame_dat), cv2.COLOR_BGR2RGB)
		ANIMATE.write(frame)


def render_map(graph, start, end):
	for y in range(len(graph)):
		for x in range(len(graph[0])):
			if graph[y][x] == MazeObject.WALL:
				color = Colors.BLACK
			elif graph[y][x] == MazeObject.START:
				color = Colors.GREEN
			elif graph[y][x] == MazeObject.SPECIAL:
				color = Colors.SPECIAL
			else:
				color = Colors.WHITE
			draw_grid(x, y, color)

	draw_grid(start[1], start[0], color=Colors.START)
	draw_grid(end[1], end[0], color=Colors.END)
	pygame.display.update()
	write_frame()


def get_color(x, y):
	global SCREEN
	return SCREEN.get_at((x * Grid.BLOCK_SIZE + Grid.BLOCK_SIZE // 2, y * Grid.BLOCK_SIZE + Grid.BLOCK_SIZE // 2))


def set_color(x, y, color, sleep_time=1):
	draw_grid(x, y, color=color)
	pygame.display.update()
	pygame.time.wait(1)
	write_frame()


def set_frontier_color(x, y):
	color = Colors.FRONTIER
	cur_color = get_color(x, y)
	if cur_color != Colors.WHITE:
		color = darker_color(cur_color)
	set_color(x, y, color)


def set_path_color(path, special_points={}):
	passed = {}
	for point in path:
		passed[point] = False

	for point in path[1:-1]:
		color = Colors.PATH
		cur_color = get_color(point[1], point[0])
		if cur_color == Colors.PATH or cur_color == Colors.SPECIAL or point in special_points or passed[point]:
			color = darker_color(cur_color)
		passed[point] = True
		set_color(point[1], point[0], color)


def visualize(algorithm, mode, graph, start, end,
		bonus_points=[], inter_points=[], teleport_points=[],
		hf=manhattan_distance, output_path=None, extra_info=None,
		just_show_maze=False
	):
	global SCREEN, CLOCK, WIN_WIDTH, WIN_HEIGHT
	pygame.init()
	WIN_HEIGHT = Grid.BLOCK_SIZE * len(graph)
	WIN_WIDTH = Grid.BLOCK_SIZE * len(graph[0])
	if just_show_maze:
		SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	else:
		SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), flags=pygame.HIDDEN)
	pygame.display.set_caption('Hello folks👋, we are US-er!')
	CLOCK = pygame.time.Clock()
	CLOCK.tick(60)

	fps = 30
	fourcc = cv2.VideoWriter_fourcc(*"mp4v")
	global ANIMATE
	
	# Start window recorder
	if not just_show_maze and output_path is not None:
		algo_name = output_path.replace('\\', '/').split('/')[-1]
		video_fileout = os.path.join(output_path, f'{algo_name}{f"_{extra_info}" if extra_info is not None else ""}.mp4')
		ANIMATE = cv2.VideoWriter(
			video_fileout, fourcc, fps, (WIN_WIDTH, WIN_HEIGHT))
	else:
		ANIMATE = None

	# Render maze
	render_map(graph, start, end)

	# Run algorithm
	if not just_show_maze:
		output = algorithm(graph, start, end, mode, bonus_points, inter_points, teleport_points, hf=hf)

	# Re-annotate special points
	for point in bonus_points:
		write_text(str(bonus_points[point]), point[1], point[0], Colors.WHITE)

	inter_id = 1
	for point in inter_points:
		write_text(str(inter_id), point[1], point[0], Colors.WHITE)
		inter_id += 1

	teleport_id_dict = {}
	teleport_id = 1
	for point in teleport_points:
		if point not in teleport_id_dict:
			teleport_id_dict[point] = teleport_id
			teleport_id_dict[teleport_points[point]] = teleport_id
			teleport_id += 1
		write_text(str(teleport_id_dict[point]), point[1], point[0], Colors.WHITE)

	# Write result
	if not just_show_maze and output_path is not None:
		algo_name = output_path.replace('\\', '/').split('/')[-1]
		result_fileout = os.path.join(output_path, f'{algo_name}{f"_{extra_info}" if extra_info is not None else ""}.txt')
		try:
			with open(result_fileout, 'w') as fp:
				if not output:
					fp.write('NO')
				else:
					fp.write(str(output))
		except Exception as err:
			print(err)
	
	try:
		if ANIMATE is not None:
			ANIMATE.release()
	except Exception as err:
		print('[EXCEPTION] video was not released.\n', err)


	if just_show_maze:
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()