import board as b
import pygame as pg
import pathfinders as pf
from queue import PriorityQueue
import cProfile
import time
from copy import deepcopy
from pygame.locals import *
import sys

WHITE = (255, 255, 255)
LIGHTER_BLUE = (102, 140, 191)
DARK_BLUE = (41, 65, 97)

# creates an intro screen that shows for a max of 10 seconds
def start_screen(window, width, button_offset):
    pg.display.set_caption('Pathfinder')

    INTRO = True

    while INTRO:
        for event in pg.event.get():
            # quit if prompted
            if event.type == pg.QUIT:
                INTRO = False
                pg.quit()
                quit()

        # create the main screen and text
        window.fill(WHITE)
        large_text = pg.font.Font('freesansbold.ttf', int(width/7))
        text_surf, text_rect = b.text_objects("Pathfinder", large_text, DARK_BLUE)
        text_rect.center = ((width/2),(width/2))
        window.blit(text_surf, text_rect)

        # create the button rectangle
        x = 0
        y = 0
        w = width / 5
        h = width / 14

        x = (width/ 2) - (w/2)
        y = (width/2) - (h/2) + button_offset

        # return true if button is not pressed
        def ret_true():
            return True

        # return false so that start screen exits
        def ret_false():
            return False
    
        INTRO = b.create_button(window, lambda: ret_true(), lambda: ret_false(), width/24, "START", LIGHTER_BLUE, DARK_BLUE, x, y, w, h)

        pg.display.update()
        pg.time.Clock().tick(120)

def main(window, rows, width, height):
    pg.display.set_caption('Pathfinder')

    ROWS = rows
    WIDTH = width
    HEIGHT = height
    WINDOW = window
    board = b.initialize_board(ROWS, WIDTH, HEIGHT)
    old_board = deepcopy(board)

    # STATUS variables
    RUNNING = True
    ALG_STARTED = False

    start_node = None
    end_node = None
    while RUNNING:
        b.draw_board(WINDOW, board, ROWS, WIDTH, HEIGHT)
        for event in pg.event.get():
            # quit if prompted
            if event.type == pg.QUIT:
                RUNNING = False
            
            # if alg has started, the user should only
            # be able to quit the program
            if ALG_STARTED:
                continue

            if pg.mouse.get_pressed():
                position = pg.mouse.get_pos()
                row, col = b.mouse_position(position, ROWS, WIDTH, HEIGHT)
                if row < ROWS:
                    node = board[row][col]

                # left click
                if pg.mouse.get_pressed()[0]:
                    if not start_node and node != end_node:
                        start_node = node
                        start_node.make_start()
                    
                    if not end_node and node != start_node:
                        end_node = node
                        end_node.make_end()

                    elif node != start_node and node != end_node:
                        node.make_wall()
                
                # right click
                if pg.mouse.get_pressed()[2]:
                    node.undo()
                    if node == start_node:
                        start_node = None
                    if node == end_node:
                        end_node = None

            if event.type == pg.KEYDOWN:

                # if r is pressed, recreate the whole board
                if event.key == pg.K_r and not ALG_STARTED:
                    board = b.initialize_board(ROWS, WIDTH, HEIGHT)
                    old_board = deepcopy(board)

                    # STATUS variables
                    RUNNING = True
                    ALG_STARTED = False

                    start_node = None
                    end_node = None
                
                # if c is pressed, clear the board
                if event.key == pg.K_c and not ALG_STARTED:
                    board = old_board
                    old_board = deepcopy(board)

                    # STATUS variables
                    RUNNING = True
                    ALG_STARTED = False

                    start_node = None
                    end_node = None

                # when spacebar is pressed, update all of the neighbors
                # and run the algorithm
                if event.key == pg.K_SPACE and not ALG_STARTED:
                    if start_node and end_node:
                        # initialize the neighbors for the algorithm
                        for row in board:
                            for node in row:
                                node.update_neighbors(board)
                        pf.a_star(lambda: b.draw_board(WINDOW, board, ROWS, WIDTH, HEIGHT), board, start_node, end_node, WIDTH, "speed")
                
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
                    sys.exit()
       
    pg.quit()
    quit()

if __name__ == "__main__":
    # some constants need to be changed with different
    # window sizes. These are what I have found to be
    # the most visually pleasing settings.

    ROWS = 20
    WIDTH = 800
    HEIGHT = 825

    pg.init()
    flags = DOUBLEBUF | RESIZABLE
    WINDOW = pg.display.set_mode((WIDTH, HEIGHT), flags)
    WINDOW.set_alpha(None)

    #WINDOW = pg.display.set_mode((WIDTH, HEIGHT))

    BUTTON_OFFSET = 150
    start_screen(WINDOW, WIDTH, BUTTON_OFFSET)
    main(WINDOW, ROWS, WIDTH, HEIGHT)
