import math
import pygame as pg
import random

# color codes
RED = (255, 0, 0)
GREEN = (163, 197, 199)
LIGHT_BLUE = (180, 210, 250)
DARK_BLUE = (41, 65, 97)
YELLOW = (248, 236, 194)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_PURPLE = (71, 41, 97)
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
        self.length = length
        self.neighbors = []
        self.color = WHITE
        self.total_rows = total_rows

        # speed lets us know the speed we can travel to get to 
        # a neighboring node
        if (highway == True):
            self.speed = 60
        else:
            self.speed = 30
        
    # draws the rectangle that represents the node
    def render(self, window):
        pg.draw.rect(window, self.color, (self.x, self.y, self.length, self.length))
    
    # nodes are identified by their colors
    def is_start(self):
        return self.color == YELLOW

    def make_start(self):
        self.color = YELLOW
    
    def is_end(self):
        return self.color == LIGHT_PURPLE

    def make_end(self):
        self.color = LIGHT_PURPLE

    def is_wall(self):
        return self.color == DARK_BLUE
        
    def make_wall(self):
        self.color = DARK_BLUE
    
    def make_path(self):
        self.color = LIGHT_BLUE
    
    # reset the node to white
    def undo(self):
        self.color = WHITE
    
    # update the neighbors for given node, excluding walls
    def update_neighbors(self, board):
        self.neighbors = []

        # check the row above
        if self.row > 0 and not board[self.row - 1][self.col].is_wall():
            self.neighbors.append(board[self.row - 1][self.col])
        
        # check the row below
        if self.row < self.total_rows - 1 and not board[self.row + 1][self.col].is_wall():
            self.neighbors.append(board[self.row + 1][self.col])
        
        # check the left col
        if self.col > 0 and not board[self.row][self.col - 1].is_wall():
            self.neighbors.append(board[self.row][self.col - 1])

        # check the right col
        if self.col < self.total_rows - 1 and not board[self.row][self.col + 1].is_wall():
            self.neighbors.append(board[self.row][self.col + 1])
        
# draws gridlines on board
def draw_grid(window, rows, width):
    length = width // rows
    for i in range(rows):
        pg.draw.line(window, GREY, (0, i * length), (width, i * length))
    for j in range(rows):
        pg.draw.line(window, GREY, (j * length, 0), (j * length, width)) 

# initializes a row x row board with nodes of correct width and random 
# highway states
def initialize_board(rows, width):
    length = width // rows
    board = []
    for i in range(rows):
        board.append([])
        for j in range(rows):
            node = Node(i, j, length, bool(random.getrandbits(1)),rows)
            board[i].append(node)
    
    return board

# draw a white board with all of the nodes and grid lines
def draw_board(window, board, rows, width):
    window.fill(WHITE)

    for row in board:
        for node in row:
            node.render(window)

    draw_grid(window, rows, width)
    pg.display.update()

# helper method to get row, col corresponding to mouse position
def mouse_position(position, rows, width):
    length = width // rows
    y, x = position
    
    row = y // length
    col = x // length

    return row, col