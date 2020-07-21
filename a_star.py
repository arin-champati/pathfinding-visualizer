import math
import pygame as pg
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

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
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    
    def position(self):
        return self.row, self.col
    
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
        
    def render(self, win):
        pygame.draw.rect(win, self.color, ())