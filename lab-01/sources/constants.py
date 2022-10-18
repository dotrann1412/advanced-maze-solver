# Maze object
class MazeObject:
    START = 'S'
    WALL = 'x'
    SPECIAL = '+'
    EMPTY = ' '

# Colors
class Colors():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 220, 0)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)

    # Special cell
    START = ORANGE
    END = BLUE
    SPECIAL = RED

    # Colors for algorithms
    FRONTIER = GREEN
    PATH = YELLOW

# Algorithms
class Algorithms():
    BFS = 'bfs'
    DFS = 'dfs'
    UCS = 'ucs'
    GBFS = 'gbfs'
    A_STAR = 'a_star'
