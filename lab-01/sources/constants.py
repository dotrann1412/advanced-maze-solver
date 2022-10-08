from enum import Enum

# Maze object
class MazeObject(Enum):
    START = 'S'
    WALL = 'x'
    BONUS = '+'
    EMPTY = ' '
    INTER = '>'
    TELE = 'o'

# Colors
class Colors(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 150, 0)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)

    # Colors for algorithms
    FRONTIER_COLOR = GREEN
    PATH_COLOR = YELLOW

# Window size
WIN_WIDTH = 400
WIN_HEIGHT = 300

# Algorithms
class Algorithms(Enum):
    BFS = 'bfs'
    DFS = 'dfs'
    UCS = 'ucs'
    GREEDY = 'greedy'
    A_STAR = 'a_star'
