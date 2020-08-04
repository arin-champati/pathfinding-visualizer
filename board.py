import math
import pygame as pg
import random
from config import Colors, Speeds

# Node represents one square on the board
class Node:
    def __init__(self, row, col, diff, length, highway, total_rows):
        self.row = row
        self.col = col
        self.x = row * length 
        self.y = col * length + diff
        self.length = length
        self.neighbors = []
        self.color = Colors.WHITE
        self.total_rows = total_rows
        self.g = float("inf")
        self.f = float("inf")
        self.parent = None
        self.highway = highway

        # speed lets us know the speed we can travel to get to 
        # a neighboring node
        if (highway == True):
            self.speed = Speeds.HIGHWAY_SPEED
            self.color = Colors.LIGHT_GREY
        else:
            self.speed = Speeds.LOCAL_SPEED
            self.color = Colors.WHITE

    # draws the rectangle that represents the node
    def render(self, window):
        return pg.draw.rect(window, self.color, (self.x, self.y, self.length, self.length))
    
    def is_rendered(self):
        return (self.is_start() or self.is_end() or self.is_wall())
    
    def position(self):
        return self.row, self.col
    
    # the cost is time
    def time(self):
        return 1/self.speed

    # nodes are identified by their color
    def is_start(self):
        return self.color == Colors.YELLOW
    
    def make_start(self):
        self.color = Colors.YELLOW
    
    def is_end(self):
        return self.color == Colors.LIGHT_PURPLE

    def make_end(self):
        self.color = Colors.LIGHT_PURPLE

    def is_wall(self):
        return self.color == Colors.DARKER_BLUE
        
    def make_wall(self):
        self.color = Colors.DARKER_BLUE
    
    def make_path(self):
        self.color = Colors.DARK_PURPLE
    
    def make_open(self):
        self.color = Colors.GREEN
    
    def make_closed(self):
        self.color = Colors.LIGHT_BLUE
    
    # reset the node to white
    def undo(self):
        if self.highway == True:
            self.color = Colors.LIGHT_GREY
        elif self.highway == False:
            self.color = Colors.WHITE
    
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
def draw_grid(window, rows, width, height):
    length = width // rows 
    begin = height - width

    for i in range(rows):
        pg.draw.line(window, Colors.GREY, (0, i * length + begin), (width, i * length + begin))
    for j in range(rows):
        pg.draw.line(window, Colors.GREY, (j * length, begin), (j * length, height)) 

# initializes a row x row board with nodes of correct width and random 
# highway states
def initialize_board(rows, width, height):
    length = width // rows
    diff = height - width
    board = []
    for i in range(rows):
        board.append([])
        for j in range(rows):
            node = Node(i, j, diff, length, bool(random.getrandbits(1)),rows)
            board[i].append(node)
    
    return board

# draw board with all of the nodes, grid lines, and also menu bar
def draw_board(window, menu, board, rows, width, height):
    window.fill(Colors.DARKER_BLUE)

    for row in board:
        for node in row:
            node.render(window)

    draw_grid(window, rows, width, height)
    menu()
    pg.display.update()

# draw board with all of the nodes, grid lines, and also menu bar
def draw_node(window, menu, board, nodes, rows, width, height):
    for node in nodes:
        node.render(window)

    draw_grid(window, rows, width, height)
    menu()
    pg.display.update()

# helper method to get row, col corresponding to mouse position
def mouse_position(position, rows, width, height):
    length = width // rows
    
    y, x = position
    diff = height - width

    x = x - diff
    
    row = y // length
    col = x // length

    return row, col