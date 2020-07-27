import board as b
from board import Node
import button
import pygame as pg
import pathfinders as pf
from queue import PriorityQueue
import cProfile
import time
from copy import deepcopy, copy
from pygame.locals import *
import sys
from config import Colors, Fonts
from nav_bar import menu
from button import create_button
import board_functionality as bf
from functools import partial
import os

# creates an intro screen that shows for a max of 10 seconds
def start_screen(window, width, button_offset):
    pg.display.set_caption('Pathfinder')

    INTRO = True

    MOUSEUP = None

    while INTRO:
        MOUSEUP = None

        for event in pg.event.get():
            # quit if prompted
            if event.type == pg.QUIT:
                INTRO = False
                pg.quit()
                quit()
            
            if event.type == MOUSEBUTTONUP and event.button == 1:
                MOUSEUP = MOUSEBUTTONUP

            if event.type == KEYDOWN:
            # exit fullscreen mode
                if event.key == K_ESCAPE:
                    flags = DOUBLEBUF
                    WINDOW = pg.display.set_mode((WIDTH, HEIGHT), flags)
                
                # enter fullscreen mode
                if event.key == pg.K_f:
                    flags = DOUBLEBUF | FULLSCREEN
                    WINDOW = pg.display.set_mode((WIDTH, HEIGHT), flags)

        # create the main screen and text
        window.fill(Colors.WHITE)
        large_text = pg.font.Font(Fonts.HOME, int(width/7))
        text_surf, text_rect = button.text_objects("Pathfinder", large_text, Colors.DARK_BLUE)
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
    
        INTRO = create_button(window, MOUSEUP, lambda: ret_true(), lambda: ret_false(), width/24, "START", Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, y, w, h)

        pg.display.update()

def main(window, rows, width, height):
    pg.display.set_caption('Pathfinder')

    ROWS = rows
    WIDTH = width
    HEIGHT = height
    WINDOW = window
    board = b.initialize_board(ROWS, WIDTH, HEIGHT)
    old_board = deepcopy(board)

    boundary_board = None

    # STATUS variables
    RUNNING = True
    ALG_STARTED = False
    ALG_FINISHED = False

    # algorith dropdown
    ALG_DROPDOWN = False
    A_STAR = False
    DIJKSTRA = False

    # metric dropdown
    METRIC_DROPDOWN = False
    DISTANCE_METRIC = True
    TIME_METRIC = False

    # board dropdown
    BOARD_DROPDOWN = False
    NEW = False
    ERASE = False
    RESET = False

    # results
    TIME = 0
    DISTANCE = 0

    start_node = None
    end_node = None

    FLAGS = DOUBLEBUF

    MOUSEUP = None

    while RUNNING:
        pg.time.Clock().tick(10000)

        ALG_STARTED = False
        
        # draw the GUI
        draw = partial(b.draw_board, WINDOW, lambda: menu(WINDOW, MOUSEUP, ALG_DROPDOWN, A_STAR, DIJKSTRA, METRIC_DROPDOWN, 
        DISTANCE_METRIC, TIME_METRIC, BOARD_DROPDOWN, NEW, ERASE, RESET, TIME, DISTANCE, WIDTH, HEIGHT), board, ROWS, WIDTH, HEIGHT)

        menu_func = partial(menu, WINDOW, MOUSEUP, ALG_DROPDOWN, A_STAR, DIJKSTRA, METRIC_DROPDOWN, 
        DISTANCE_METRIC, TIME_METRIC, BOARD_DROPDOWN, NEW, ERASE, RESET, TIME, DISTANCE, WIDTH, HEIGHT)

        draw()

        # get the states of important STATUS variables
        ALG_DROPDOWN, A_STAR, DIJKSTRA, METRIC_DROPDOWN, DISTANCE_METRIC, TIME_METRIC, BOARD_DROPDOWN, NEW, ERASE, RESET, TIME, DISTANCE = menu(WINDOW, MOUSEUP, ALG_DROPDOWN, A_STAR, DIJKSTRA, METRIC_DROPDOWN, 
        DISTANCE_METRIC, TIME_METRIC, BOARD_DROPDOWN, NEW, ERASE, RESET, TIME, DISTANCE, WIDTH, HEIGHT)

        if NEW == True:
            NEW, ALG_STARTED, ALG_FINISHED, board, old_board, start_node, end_node = bf.new_board(ROWS, WIDTH, HEIGHT)

        if ERASE == True:
            ERASE, ALG_STARTED, ALG_FINISHED, board, old_board, start_node, end_node = bf.erase_board(old_board)
        
        if RESET == True:
            RESET, ALG_STARTED, ALG_FINISHED, board, old_board, start_node, end_node = bf.reset_board(ALG_STARTED, ALG_FINISHED, board, boundary_board, start_node, end_node)

        MOUSEUP = None
        
        for event in pg.event.get():
            # quit if prompted
            if event.type == pg.QUIT:
                RUNNING = False
            
            # if alg has started, the user should only
            # be able to quit the program
            if ALG_STARTED:
                continue
            
            if event.type == MOUSEBUTTONUP and event.button == 1:
                MOUSEUP = MOUSEBUTTONUP
        
            # only get position of mouse if pressed and the menus are closed
            if pg.mouse.get_pressed():

                if (ALG_DROPDOWN != True and METRIC_DROPDOWN != True and BOARD_DROPDOWN != True):
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
                        if ALG_FINISHED:
                            RESET, ALG_STARTED, ALG_FINISHED, board, boundary_board, start_node, end_node = bf.reset_board(ALG_STARTED, ALG_FINISHED, board, boundary_board, start_node, end_node)
                                
                        if not ALG_FINISHED:
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
                        if ALG_FINISHED:
                            RESET, ALG_STARTED, ALG_FINISHED, board, boundary_board, start_node, end_node = bf.reset_board(ALG_STARTED, ALG_FINISHED, board, boundary_board, start_node, end_node)
                                
                        if not ALG_FINISHED:
                            node.undo()
                            if node == start_node:
                                start_node = None
                            if node == end_node:
                                end_node = None

            if event.type == pg.KEYDOWN:

                # quit
                if event.key == pg.K_q:
                    RUNNING = False

                if FLAGS == DOUBLEBUF | FULLSCREEN:
                    # exit fullscreen mode
                    if event.key == pg.K_ESCAPE:                    
                        FLAGS = DOUBLEBUF
                        WINDOW = pg.display.set_mode((WIDTH, HEIGHT), FLAGS)

                if FLAGS == DOUBLEBUF:
                    # enter fullscreen mode
                    if event.key == pg.K_f:
                        FLAGS = DOUBLEBUF | FULLSCREEN
                        WINDOW = pg.display.set_mode((WIDTH, HEIGHT), FLAGS)

                # if n is pressed, recreate the whole board
                if event.key == pg.K_n and not ALG_STARTED:
                    NEW, ALG_STARTED, ALG_FINISHED, board, old_board, start_node, end_node = bf.new_board(ROWS, WIDTH, HEIGHT)
                
                # if e is pressed, erase the board
                if event.key == pg.K_e and not ALG_STARTED:
                    ERASE, ALG_STARTED, ALG_FINISHED, board, old_board, start_node, end_node = bf.erase_board(old_board)
                
                if event.key == pg.K_r:
                    RESET, ALG_STARTED, ALG_FINISHED, board, boundary_board, start_node, end_node = bf.reset_board(ALG_STARTED, ALG_FINISHED, board, boundary_board, start_node, end_node)

                if ALG_FINISHED:
                    RESET, ALG_STARTED, ALG_FINISHED, board, boundary_board, start_node, end_node = bf.reset_board(ALG_STARTED, ALG_FINISHED, board, boundary_board, start_node, end_node)
                    draw = partial(b.draw_board, WINDOW, lambda: menu(WINDOW, MOUSEUP, ALG_DROPDOWN, A_STAR, DIJKSTRA, METRIC_DROPDOWN, 
                    DISTANCE_METRIC, TIME_METRIC, BOARD_DROPDOWN, NEW, ERASE, RESET, TIME, DISTANCE, WIDTH, HEIGHT), board, ROWS, WIDTH, HEIGHT)
                    
                    draw()

                # RUN A STAR

                # when key a is pressed or space is pressed (and we have selected a star as our algorithm with distance as metric) (default to this setting if nothing selected)
                # update the neighbors and run the algorithm
                if (event.key == pg.K_a or (event.key == pg.K_SPACE and (A_STAR == True or DIJKSTRA == False) and (DISTANCE_METRIC == True or TIME_METRIC == False))) and not ALG_STARTED:
                    if not ALG_FINISHED:
                        boundary_board = deepcopy(board)

                        if start_node and end_node:
                            ALG_FINISHED, TIME, DISTANCE = pf.a_star(WINDOW, lambda: draw(), lambda: menu_func(), board, start_node, end_node, ROWS, WIDTH, HEIGHT, "distance")

                # when key s is pressed or space is pressed (and we have selected a star as our algorithm with time as metric)
                # update the neighbors and run the algorithm
                if (event.key == pg.K_s or (event.key == pg.K_SPACE and (A_STAR == True or DIJKSTRA == False) and (TIME_METRIC == True))) and not ALG_STARTED:
                    boundary_board = deepcopy(board)
                    if not ALG_FINISHED:
                        if start_node and end_node:
                            ALG_FINISHED, TIME, DISTANCE = pf.a_star(WINDOW, lambda: draw(), lambda: menu_func(), board, start_node, end_node, ROWS, WIDTH, HEIGHT, "time")

                if (event.key == pg.K_d or (event.key == pg.K_SPACE and (DIJKSTRA == True) and (DISTANCE_METRIC == True or TIME_METRIC == False))) and not ALG_STARTED:
                    if not ALG_FINISHED:
                        boundary_board = deepcopy(board)

                        if start_node and end_node:
                            ALG_FINISHED, TIME, DISTANCE = pf.dijkstra(WINDOW, lambda: draw(), lambda: menu_func(), board, start_node, end_node, ROWS, WIDTH, HEIGHT, "distance")

                # when key s is pressed or space is pressed (and we have selected a star as our algorithm with time as metric)
                # update the neighbors and run the algorithm
                if (event.key == pg.K_y or (event.key == pg.K_SPACE and (DIJKSTRA == True) and (TIME_METRIC == True))) and not ALG_STARTED:
                    boundary_board = deepcopy(board)
                    if not ALG_FINISHED:
                        if start_node and end_node:
                            ALG_FINISHED, TIME, DISTANCE = pf.dijkstra(WINDOW, lambda: draw(), lambda: menu_func(), board, start_node, end_node, ROWS, WIDTH, HEIGHT, "time")


       
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
    # create the button rectangle
    x = 0
    y = 0

    pg.init()

    flags = DOUBLEBUF
    WINDOW = pg.display.set_mode((WIDTH, HEIGHT), flags)
    WINDOW.set_alpha(None)
    #SDL_SetWindowSize(m_pWindow, m_width, m_height)
    #SDL_SetWindowPosition(m_pWindow, SDL_WINDOWPOS_CENTERED, 
    #SDL_WINDOWPOS_CENTERED)

    BUTTON_OFFSET = 150
    start_screen(WINDOW, WIDTH, BUTTON_OFFSET)
    main(WINDOW, ROWS, WIDTH, HEIGHT)