# Maze object
class MazeObject():
    START = 'S'
    WALL = 'x'
    BONUS = '+'
    EMPTY = ' '
    INTER = '>'
    TELE = 'o'

# Colors
class Colors():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    RED_LIGHT = (255, 100, 100)
    GREEN = (0, 150, 0)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)

    # Special cell
    START_COLOR = ORANGE
    END_COLOR = BLUE
    BONUS_COLOR = RED
    BONUS_PASSED = RED_LIGHT

    # Colors for algorithms
    FRONTIER_COLOR = GREEN
    PATH_COLOR = YELLOW

# Window size
WIN_WIDTH = 400
WIN_HEIGHT = 300

# Algorithms
class Algorithms():
    BFS = 'bfs'
    DFS = 'dfs'
    UCS = 'ucs'
    GBFS = 'gbfs'
    A_STAR = 'a_star'
