import board as b
import pygame as pg
import pathfinders as pf
from queue import PriorityQueue
import cProfile
import time

pg.init()

LIGHT_BLUE = (102, 140, 191)
DARK_BLUE = (41, 65, 97)
WHITE = (255, 255, 255)

# render text objects
def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

# create a button with specified macros
def create_button(window, action, font_size, text, active_color, inactive_color, x, y, w, h):
    mouse = pg.mouse.get_pos()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pg.draw.rect(window, active_color, (x, y, w, h))
        if pg.mouse.get_pressed()[0]:
            result = action()
            return result
    else:
        pg.draw.rect(window, inactive_color, (x, y, w, h))

    small_text = pg.font.Font('freesansbold.ttf', int(font_size))
    text_surf, text_rect = text_objects(text, small_text, WHITE)
    text_rect.center = ((x + (w/2), y + (h / 2)))
    window.blit(text_surf, text_rect)

    return True

# creates an intro screen that shows for a max of 10 seconds
def start_screen(window, width, button_offset):
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
        text_surf, text_rect = text_objects("Pathfinder", large_text, DARK_BLUE)
        text_rect.center = ((width/2),(width/2))
        window.blit(text_surf, text_rect)

        # create the button rectangle
        x = 0
        y = 0
        w = width / 5
        h = width / 14

        x = (width/ 2) - (w/2)
        y = (width/2) - (h/2) + button_offset

        INTRO = create_button(window, lambda: False, width/24, "START", LIGHT_BLUE, DARK_BLUE, x, y, w, h)

        pg.display.update()
        pg.time.Clock().tick(10)
            


def main(window, rows, width, height):
    ROWS = rows
    WIDTH = width
    HEIGHT = height
    WINDOW = window
    board = b.initialize_board(ROWS, WIDTH, HEIGHT)

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
                if row < ROWS - 1:
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

                # if c is pressed, restart the whole board
                if event.key == pg.K_r and not ALG_STARTED:
                    board = b.initialize_board(ROWS, WIDTH, HEIGHT)
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
                        pf.a_star(lambda: b.draw_board(WINDOW, board, ROWS, WIDTH, HEIGHT), board, start_node, end_node)
            
    pg.quit()
    quit()

if __name__ == "__main__":
    # some constants need to be changed with different
    # window sizes. These are what I have found to be
    # the most visually pleasing settings.

    ROWS = 20
    WIDTH = 800
    HEIGHT = 825
    WINDOW = pg.display.set_mode((WIDTH, HEIGHT))

    BUTTON_OFFSET = 150
    start_screen(WINDOW, WIDTH, BUTTON_OFFSET)
    main(WINDOW, ROWS, WIDTH, HEIGHT)
