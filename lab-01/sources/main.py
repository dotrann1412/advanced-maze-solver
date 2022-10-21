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
        'EUCLIDEAN': euclidean_distance,
        'MANHATTAN': manhattan_distance
    }

    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--algorithms", help="Algorithm to run",
                        choices=AlgorithmsMapping.keys(), type=str, required=True)
    parser.add_argument("-m", "--mode", help="Running mode",
                        choices=[AlgorithmsMode.NORMAL.name, AlgorithmsMode.TELEPORT.name, AlgorithmsMode.BONUS.name, AlgorithmsMode.INTERMEDIATE.name],
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
    output_dir = None

    if args.algorithms:
        algorithm = AlgorithmsMapping[args.algorithms]

    if args.mode:
        mode = AlgorithmsMode[args.mode]

    if args.input:
        input_file = args.input

    if args.heuristic_function:
        heuristic = HeuristicMapping[args.heuristic_function]

    if args.output:
        output_dir = args.output
        if not os.path.exists(output_dir):
            print(f'[*][ERROR] Folder not found! {output_dir}')
            exit(1)
        elif os.path.isfile(output_dir):
            print(f'[*][WARNING] {output_dir} may not be a directory.')

    files = []
    if os.path.isfile(input_file):
        files = [input_file]
    else:
        files = [file for file in os.listdir(input_file) 
                    if os.path.isfile(os.path.join(input_file, file))]
    
    algoname = args.algorithms.lower().replace('_', '')

    for file in files:
        matrix, start, end, bonus_points, inter_points, teleport_points = read_file (
            os.path.join(input_file, file), 
            mode
        )

        dest = os.path.join(output_dir, f'level_{mode.value}', f'map_{os.path.splitext(file)[0]}', algoname)
        mkdir_plus(dest)

        try:
            visualize(
                algorithm, mode, matrix, start, end,
                bonus_points, inter_points, teleport_points,
                hf=heuristic,
                output_path=dest
            )
        except BrokenPipeError:
            continue