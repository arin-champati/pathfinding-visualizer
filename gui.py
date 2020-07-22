import board as b
import pygame as pg
import pathfinders as pf
from queue import PriorityQueue
import cProfile
import time
from copy import deepcopy
from pygame.locals import *
import sys
import colors
from nav_bar import menu
from button import create_button

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

            if event.type == pg.KEYDOWN:
            # exit fullscreen mode
                if event.key == pg.K_ESCAPE:
                    flags = DOUBLEBUF
                    WINDOW = pg.display.set_mode((WIDTH, HEIGHT), flags)
                
                # enter fullscreen mode
                if event.key == pg.K_f:
                    flags = DOUBLEBUF | FULLSCREEN
                    WINDOW = pg.display.set_mode((WIDTH, HEIGHT), flags)

        # create the main screen and text
        window.fill(colors.WHITE)
        large_text = pg.font.Font('freesansbold.ttf', int(width/7))
        text_surf, text_rect = b.text_objects("Pathfinder", large_text, colors.DARK_BLUE)
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
    
        INTRO = create_button(window, lambda: ret_true(), lambda: ret_false(), width/24, "START", colors.LIGHTER_BLUE, colors.DARK_BLUE, x, y, w, h)

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

    # algorith dropdown
    ALG_DROPDOWN = False
    A_STAR = False
    DIJKSTRA = False

    # metric dropdown
    METRIC_DROPDOWN = False
    DISTANCE = False
    TIME = False

    start_node = None
    end_node = None
    while RUNNING:
        pg.time.Clock().tick(120)

        # draw the GUI
        b.draw_board(WINDOW, lambda: menu(WINDOW, ALG_DROPDOWN, A_STAR, DIJKSTRA, METRIC_DROPDOWN, 
        DISTANCE, TIME, WIDTH, HEIGHT), board, ROWS, WIDTH, HEIGHT)

        # get the states of important STATUS variables
        ALG_DROPDOWN, A_STAR, DIJKSTRA, METRIC_DROPDOWN, DISTANCE, TIME = menu(WINDOW, ALG_DROPDOWN, 
        A_STAR, DIJKSTRA, METRIC_DROPDOWN, DISTANCE, TIME, WIDTH, HEIGHT)

        for event in pg.event.get():
            # quit if prompted
            if event.type == pg.QUIT:
                RUNNING = False
            
            # if alg has started, the user should only
            # be able to quit the program
            if ALG_STARTED:
                continue

            # only get position of mouse if pressed and the menus are closed
            if pg.mouse.get_pressed() and (ALG_DROPDOWN != True and METRIC_DROPDOWN != True):
                position = pg.mouse.get_pos()
                _, y = position

                # make sure we are not in the navigation area
                if (y < (HEIGHT - WIDTH)):
                    continue
                
                row, col = b.mouse_position(position, ROWS, WIDTH, HEIGHT)
                if row < ROWS and col < ROWS:
                    node = board[row][col]

                # LEFT click
                if pg.mouse.get_pressed()[0]:
                    if not start_node and node != end_node:
                        start_node = node
                        start_node.make_start()
                    
                    if not end_node and node != start_node:
                        end_node = node
                        end_node.make_end()

                    elif node != start_node and node != end_node:
                        node.make_wall()
                
                # RIGHT click
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

                # RUN A STAR

                # when key s is pressed or space is pressed (and we have selected a star as our algorithm with time as metric (default to this setting if nothing selected))
                # update the neighbors and run the algorithm
                if (event.key == pg.K_s or (event.key == pg.K_SPACE and (A_STAR == True or DIJKSTRA == False) and (TIME == True or (DISTANCE == False and TIME == False)))) and not ALG_STARTED:
                    if start_node and end_node:
                        # initialize the neighbors for the algorithm
                        for row in board:
                            for node in row:
                                node.update_neighbors(board)
                        pf.a_star(lambda: b.draw_board(WINDOW, lambda: menu(WINDOW, ALG_DROPDOWN, A_STAR, DIJKSTRA, METRIC_DROPDOWN, DISTANCE, TIME, WIDTH, HEIGHT), 
                        board, ROWS, WIDTH, HEIGHT), board, start_node, end_node, WIDTH, "speed")
                
                # when key a is pressed or space is pressed (and we have selected a star as our algorithm with distance as metric)
                # update the neighbors and run the algorithm
                if (event.key == pg.K_a or (event.key == pg.K_SPACE and (A_STAR == True or DIJKSTRA == False) and DISTANCE == True)) and not ALG_STARTED:
                    if start_node and end_node:
                        # initialize the neighbors for the algorithm
                        for row in board:
                            for node in row:
                                node.update_neighbors(board)
                        pf.a_star(lambda: b.draw_board(WINDOW,lambda: menu(WINDOW, ALG_DROPDOWN, A_STAR, DIJKSTRA, METRIC_DROPDOWN, DISTANCE, TIME, WIDTH, HEIGHT), 
                        board, ROWS, WIDTH, HEIGHT), board, start_node, end_node, WIDTH, "distance")
                
                # exit fullscreen mode
                if event.key == pg.K_ESCAPE:
                    flags = DOUBLEBUF
                    WINDOW = pg.display.set_mode((WIDTH, HEIGHT), flags)
                
                # enter fullscreen mode
                if event.key == pg.K_f:
                    flags = DOUBLEBUF | FULLSCREEN
                    WINDOW = pg.display.set_mode((WIDTH, HEIGHT), flags)
       
    pg.quit()
    quit()

if __name__ == "__main__":
    # some constants need to be changed with different
    # window sizes. These are what I have found to be
    # the most visually pleasing settings.

    # Note: height must be greater than width

    ROWS = 25
    WIDTH = 800
    HEIGHT = 825

    pg.init()
    flags = DOUBLEBUF
    WINDOW = pg.display.set_mode((WIDTH, HEIGHT), flags)
    WINDOW.set_alpha(None)

    #WINDOW = pg.display.set_mode((WIDTH, HEIGHT))

    BUTTON_OFFSET = 150
    #start_screen(WINDOW, WIDTH, BUTTON_OFFSET)
    main(WINDOW, ROWS, WIDTH, HEIGHT)
