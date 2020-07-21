import math
import pygame as pg
from queue import PriorityQueue
import random

WIDTH = 800
WINDOW = pg.display.set_mode((WIDTH, WIDTH))
pg.display.set_caption("A* Path Finding Algorithm")

# color codes
RED = (255, 0, 0)
GREEN = (163, 197, 199)
LIGHT_BLUE = (180, 210, 250)
DARK_BLUE = (41, 65, 97)
YELLOW = (248, 236, 194)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (71, 41, 97)
LIGHT_PURPLE = (218, 180, 250)
BURNT_ORANGE = (206, 140, 117)
SALMON = (250, 188, 180)
GREY = (128, 128, 128)
TURQOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, length, highway, total_rows):
        self.row = row
        self.col = col
        self.x = row * length
        self.y = col * length
        self.color = WHITE
        self.neighbors = []
        self.length = length

        # speed lets us know the speed we can travel to get to 
        # a neighboring node
        if (highway == True):
            self.speed = 60
        else:
            self.speed = 30

        self.total_rows = total_rows
    
    def position(self):
        return self.row, self.col
    
    def time(self):
        return 1/self.speed
    
    # methods for checking what state a node is in
    def is_start(self):
        return self.color == YELLOW
    
    def is_end(self):
        return self.color == LIGHT_PURPLE

    def is_wall(self):
        return self.color == BURNT_ORANGE
    
    def is_closed(self):
        return self.color == DARK_BLUE
    
    def is_open(self):
        return self.color == GREEN
    
    # methods for changing the state of a node
    def make_white(self):
        self.color = WHITE
    
    def make_start(self):
        self.color = YELLOW
    
    def make_end(self):
        self.color = LIGHT_PURPLE

    def make_wall(self):
        self.color = BURNT_ORANGE
    
    def make_closed(self):
        self.color = DARK_BLUE
    
    def make_open(self):
        self.color = LIGHT_BLUE
    
    def make_path(self):
        self.color = LIGHT_BLUE
        
    def render(self, window):
        pg.draw.rect(window, self.color, (self.x, self.y, self.length, self.length))
    
    # manhattan heuristic with 'time' as cost
def manhattan(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return self.time * (dx + dy)

    def __lt__(self, other):
        return False

# creates a list of lists that contain nodes
def make_board(rows, width):
    board = []
    length = width // rows
    for i in range(rows):
        board.append([])
        for j in range(rows):
            node = Node(i, j, length, bool(random.getrandbits(1)),rows)
            board[i].append(node)
    
    return board

# draw the grid line separators
def draw_grid_lines(window, rows, width):
    length = width // rows
    for i in range(rows):
        pg.draw.line(window, GREY, (0, i * length), (width, i * length))
    for j in range(rows):
        pg.draw.line(window, GREY, (j * length, 0), (j * length, width)) 

# display the board
def render_board(window, board, rows, width):
    window.fill(WHITE)

    for row in board:
        for node in row:
            node.render(window)
    
    draw_grid_lines(window, rows, width)
    pg.display.update()

# helper method that finds position of mouse
def get_mouse_position(position, rows, width):
    length = width // rows
    y, x = position

    row = y // length
    col = x // length

    return row, col

def main(window, width):
    ROWS = 50
    board = make_board(ROWS, width)

    start = None
    end = None

    running = True
    started = False

    while running:
        render_board(window, board, ROWS, width)
        for event in pg.event.get():
            # quit if prompted
            if event.type == pg.QUIT:
                running = False

            # if algorithm is running, only allow user to quit
            if started:
                continue
            
            # left button
            if pg.mouse.get_pressed()[0]: 
                position = pg.mouse.get_pos()
                row, col = get_mouse_position(position, ROWS, width)
                node = board[row][col]

                # if we don't have a start or end yet, make them
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                # otherwise, make a barrier
                elif node != start and node != end:
                    node.make_wall()

            # right button
            elif pg.mouse.get_pressed()[2]: 
                position = pg.mouse.get_pos()
                row, col = get_mouse_position(position, ROWS, width)
                node = board[row][col]
                node.make_white()
                if node == start:
                    start = None
                
                if node  == end:
                    end = None

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE  and not started:
                    pass
    pg.quit()

main(WINDOW, WIDTH)