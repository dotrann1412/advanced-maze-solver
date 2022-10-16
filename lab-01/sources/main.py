from constants import *
from visualizer import visualize
from utils import read_file
import argparse
import sys
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
        'EUCLIDEAN': euclidean_distance,
        'MANHATTAN': manhattan_distance
    }

    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--algorithms", help="Algorithm to run",
                        choices=AlgorithmsMapping.keys(), type=str, required=True)
    parser.add_argument("-m", "--mode", help="Running mode",
                        choices=[AlgorithmsMode.NORMAL.name, AlgorithmsMode.TELEPORT_POINT.name, AlgorithmsMode.BONUS_POINT.name, AlgorithmsMode.INTERMEDIATE_POINT.name],
                        type=str, required=True)
    parser.add_argument("-hf", "--heuristic-function", help="Heuristic function",
                        choices=HeuristicMapping.keys(),
                        type=str, default='MANHATTAN')
    parser.add_argument("-i", "--input", help="Maze input file",
                        type=str, required=True)
    parser.add_argument("-o", "--output",
                        help="Folder to save visualization output video and statistical information",
                        type=str, default=None)

    args = parser.parse_args()


    algorithm = None  # function
    mode = None  # enum
    heuristic = None
    input_file = None
    output_file = None

    if args.algorithms:
        algorithm = AlgorithmsMapping[args.algorithms]

    if args.mode:
        mode = AlgorithmsMode[args.mode]

    if args.input:
        input_file = args.input

    if args.heuristic_function:
        heuristic = HeuristicMapping[args.heuristic_function]
    
    if args.output:
        output_file = args.output

    matrix, start, end, bonus_points, inter_points, teleport_points = read_file(
        input_file, mode)

    print(f'The height of the matrix: {len(matrix)}')
    print(f'The width of the matrix: {len(matrix[0])}')
    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')

    visualize(
        algorithm, mode, matrix, start, end,
        bonus_points, inter_points, teleport_points,
        hf=heuristic,
        output_path=output_file
    )
