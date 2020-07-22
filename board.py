import math
import pygame as pg
import random
import colors

class Node:
    def __init__(self, row, col, diff, length, highway, total_rows):
        self.row = row
        self.col = col
        self.x = row * length 
        self.y = col * length + diff
        self.length = length
        self.neighbors = []
        self.color = colors.WHITE
        self.total_rows = total_rows
        self.g = float("inf")
        self.f = float("inf")
        self.parent = None

        # speed lets us know the speed we can travel to get to 
        # a neighboring node
        if (highway == True):
            self.speed = 70
            self.color = colors.LIGHT_GREY
        else:
            self.speed = 35
            self.color = colors.WHITE

    # draws the rectangle that represents the node
    def render(self, window):
        return pg.draw.rect(window, self.color, (self.x, self.y, self.length, self.length))
    
    def position(self):
        return self.row, self.col
    
    # the cost is time
    def cost(self):
        return 1/self.speed

    # nodes are identified by their colors
    def is_start(self):
        return self.color == colors.YELLOW

    def make_start(self):
        self.color = colors.YELLOW
    
    def is_end(self):
        return self.color == colors.LIGHT_PURPLE

    def make_end(self):
        self.color = colors.LIGHT_PURPLE

    def is_wall(self):
        return self.color == colors.DARK_BLUE
        
    def make_wall(self):
        self.color = colors.DARK_BLUE
    
    def make_path(self):
        self.color = colors.DARK_PURPLE
    
    def make_open(self):
        self.color = colors.GREEN
    
    def make_closed(self):
        self.color = colors.LIGHT_BLUE
    
    # reset the node to white
    def undo(self):
        self.color = colors.WHITE
    
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
        pg.draw.line(window, colors.GREY, (0, i * length + begin), (width, i * length + begin))
    for j in range(rows):
        pg.draw.line(window, colors.GREY, (j * length, begin), (j * length, height)) 

# initializes a row x row board with nodes of correct width and random 
# highway states
def initialize_board(rows, width, height):
    length = width // rows
    diff = height - width
    board = []
    random.seed(1)
    for i in range(rows):
        board.append([])
        for j in range(rows):
            node = Node(i, j, diff, length, bool(random.getrandbits(1)),rows)
            board[i].append(node)
    
    return board

# draw a white board with all of the nodes and grid lines
def draw_board(window, board, rows, width, height):
    window.fill(colors.WHITE)

    for row in board:
        for node in row:
            node.render(window)

    draw_grid(window, rows, width, height)
    pg.display.update()
    pg.time.Clock().tick(120)

# function to reset the board
def reset(window, board, rows, width, height):
    board = initialize_board(rows, width, height)
    draw_board(window, board, rows, width, height)


# helper method to get row, col corresponding to mouse position
def mouse_position(position, rows, width, height):
    length = width // rows
    
    y, x = position
    diff = height - width

    y = y
    x = x - diff
    
    row = y // length
    col = x // length

    return row, col

# get the parameters needed to write text (surface and rectangle)
def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

# create a button with specified macros
def create_button(window, default, action, font_size, text, active_color, inactive_color, x, y, w, h):
    mouse = pg.mouse.get_pos()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pg.draw.rect(window, active_color, (x, y, w, h))
        if pg.mouse.get_pressed()[0]:
            result = action()
            return result
    else:
        pg.draw.rect(window, inactive_color, (x, y, w, h))

    small_text = pg.font.Font('freesansbold.ttf', int(font_size))
    text_surf, text_rect = text_objects(text, small_text, colors.WHITE)
    text_rect.center = ((x + (w/2), y + (h / 2)))
    window.blit(text_surf, text_rect)

    return default()