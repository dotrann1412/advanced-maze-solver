from constants import *
from visualizer import visualize
from utils import mkdir_plus, read_file
import argparse
import sys, os, stat
from utils import euclidean_distance, manhattan_distance

from algorithms import a_star, bfs, dfs, ucs, gbfs
from algorithms.algorithms_utils import AlgorithmsMode

if __name__ == "__main__":
	AlgorithmsMapping = {
		'A_STAR': a_star.a_star,
		'BFS': bfs.bfs,
		'DFS': dfs.dfs,
		'UCS': ucs.ucs,
		'GBFS': gbfs.gbfs
	}

	HeuristicMapping = {
		'2': euclidean_distance,
		'1': manhattan_distance
	}

	parser = argparse.ArgumentParser()

	parser.add_argument("-a", "--algorithms", help="Algorithm to run",
						choices=AlgorithmsMapping.keys(), type=str, required=True)
	parser.add_argument("-m", "--mode", help="Running mode",
						choices=[AlgorithmsMode.NORMAL.name, AlgorithmsMode.TELEPORT.name, AlgorithmsMode.BONUS.name, AlgorithmsMode.INTERMEDIATE.name],
						type=str, required=True)
	parser.add_argument("-hf", "--heuristic-function", help="Heuristic function. 1: use manhattan; 2: use euclidean.",
						choices=HeuristicMapping.keys(),
						type=str, default='1')
	parser.add_argument("-i", "--input", help="Maze input file",
						type=str, required=True)
	parser.add_argument("-o", "--output",
						help="Folder to save visualization output video and statistical information",
						type=str, default=None)
	parser.add_argument("-jsm", "--just-show-maze", help="Visualize the maze without running any algorithm",
						type=bool, default=False)

	args = parser.parse_args()

	algorithm = None  # function
	mode = None  # enum
	heuristic = None
	input_path = None
	output_dir = None
	extra_info = None
	just_show_maze = None

	if args.mode:
		mode = AlgorithmsMode[args.mode]

	if args.algorithms:
		algorithm = AlgorithmsMapping[args.algorithms]
		if mode == AlgorithmsMode.NORMAL and (args.algorithms == 'A_STAR' or args.algorithms == 'GBFS'):
			extra_info = f'heuristic_{args.heuristic_function}'

	if args.input:
		input_path = args.input.replace('\\', '/')

	if args.heuristic_function:
		heuristic = HeuristicMapping[args.heuristic_function]

	if args.output:
		output_dir = args.output
		if not os.path.exists(output_dir):
			print(f'[*][ERROR] Folder not found! {output_dir}')
			exit(1)
		elif os.path.isfile(output_dir):
			print(f'[*][WARNING] {output_dir} may not be a directory.')

	if args.just_show_maze:
		just_show_maze = args.just_show_maze

	files = []
	if os.path.isfile(input_path):
		files = [input_path.split('/')[-1]]
		input_path = os.path.dirname(input_path)
	else:
		files = [file for file in os.listdir(input_path) 
					if os.path.isfile(os.path.join(input_path, file))]
	
	algoname = args.algorithms.lower().replace('_', '')

	for file in files:
		path = os.path.join(input_path, file).replace('\\', '/')
		print('Processing file: ', path)
		matrix, start, end, bonus_points, inter_points, teleport_points = read_file (
			path, 
			mode
		)

		if not just_show_maze and output_dir is not None:
			dest = os.path.join(output_dir, f'level_{mode.value}' if mode.value != 'advance' else 'advance', os.path.splitext(file)[0], algoname)
			mkdir_plus(dest)
		else:
			dest = None

		try:
			visualize(
				algorithm, mode, matrix, start, end,
				bonus_points, inter_points, teleport_points,
				hf=heuristic,
				output_path=dest, 
				extra_info=extra_info,
				just_show_maze=just_show_maze
			)
		except BrokenPipeError:
			continue