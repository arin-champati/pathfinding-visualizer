import pygame as pg
from config import Colors
from node import Node
import random

def draw_grid(window, rows, width, height):
    """
    window: (pygame window)
    rows: (int) number of rows
    width: (int) pixel width of board
    height: (int) pixel height of board

    summary: draws the gridlines in the given window
    """
    length = width // rows 
    begin = height - width

    for i in range(rows):
        pg.draw.line(window, Colors.GRID, (0, i * length + begin), (width, i * length + begin))
    for j in range(rows):
        pg.draw.line(window, Colors.GRID, (j * length, begin), (j * length, height)) 

def initialize_board(rows, width, height):
    """
    rows: (int) number of rows
    width: (int) pixel width of board
    height: (int) pixel height of board

    summary: initializes a row x row board filled with nodes that have random highway states
    """
    length = width // rows
    diff = height - width
    board = []
    for i in range(rows):
        board.append([])
        for j in range(rows):
            node = Node(i, j, diff, length, bool(random.getrandbits(1)),rows)
            board[i].append(node)
    
    return board

def draw_board(window, menu, board, rows, width, height):
    """
    window: (pygame window)
    menu: (lambda function) function that draws the menu bar
    board: (list) list of lists of nodes
    rows: (int) number of rows
    width: (int) pixel width of board
    height: (int) pixel height of board

    summary: renders the background, every node of the board, 
    the gridlines, and the menu
    """
    window.fill(Colors.WINDOW)

    for row in board:
        for node in row:
            node.render(window)

    draw_grid(window, rows, width, height)
    menu()
    pg.display.update()

def draw_node(window, menu, board, nodes, rows, width, height):
    """
    window: (pygame window)
    menu: (lambda function) function that draws the menu bar
    board: (list) list of lists of nodes
    rows: (int) number of rows
    width: (int) pixel width of board
    height: (int) pixel height of board

    summary: renders the given nodes, the gridlines, and the menu
    """
    for node in nodes:
        node.render(window)

    draw_grid(window, rows, width, height)
    menu()
    pg.display.update()

# helper method to get row, col corresponding to mouse position
def mouse_position(position, rows, width, height):
    """
    position: (tuple) y, x pixel position of mouse
    rows: (int) number of rows
    width: (int) pixel width of board    
    height: (int) pixel height of board
    """
    length = width // rows
    
    y, x = position
    diff = height - width

    x = x - diff
    
    row = y // length
    col = x // length

    return row, col