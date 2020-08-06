class Colors:
    # Color scheme
    GREEN = (163, 197, 199)
    LIGHT_BLUE = (180, 210, 255)
    LIGHTER_BLUE = (102, 140, 191)
    DARK_BLUE = (41, 65, 97)
    DARKER_BLUE = (35, 50, 85)
    YELLOW = (248, 236, 194)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    DARK_PURPLE = (71, 41, 97)
    LIGHT_PURPLE = (218, 180, 250)
    GREY = (128, 128, 128)
    LIGHT_GREY = (220, 220, 220)
    TURQOISE = (64, 224, 208)

    # Change these variables to affect the color scheme in game

    # Node colors
    START = YELLOW
    END = LIGHT_PURPLE
    WALL = DARKER_BLUE
    PATH = DARK_PURPLE # final path color
    OPEN = GREEN
    CLOSED = LIGHT_BLUE

    LOCAL = WHITE # local speed color
    HIGHWAY = LIGHT_GREY # highway speed color

    # Window colors
    GRID = GREY
    WINDOW = DARKER_BLUE

    # Text/button colors
    BUTTON_HOVER = LIGHTER_BLUE
    BUTTON_DEFAULT = DARK_BLUE
    TEXT = WHITE
    START_SCREEN_TEXT = DARK_BLUE


class Fonts:
    BUTTON = 'freesansbold.ttf'
    HOME = 'freesansbold.ttf'

# Node speeds
class Speeds:
    HIGHWAY_SPEED = 75
    LOCAL_SPEED = 35

# Render speeds for the algorithms
class AlgorithmRender:
    A_STAR_RENDER = 240
    DIJKSATRA_RENDER = 10000
    BFS_RENDER = 10000
    DFS_RENDER = 10000
