import board as b
import pygame as pg

def main(window, rows, width):
    ROWS = rows
    WIDTH = width
    board = b.initialize_board(ROWS, WIDTH)

    # STATUS variables
    RUNNING = True
    ALG_STARTED = False

    start_node = None
    end_node = None

    while RUNNING:
        b.draw_board(WINDOW, board, ROWS, WIDTH)
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
                row, col = b.mouse_position(position, ROWS, WIDTH)
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

            # when spacebar is pressed, update all of the neighbors
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not ALG_STARTED:
                    # initialize the neighbors for the algorithm
                    for row in board:
                        for node in row:
                            node.update_neighbors(board)
                                        

    pg.quit()

if __name__ == "__main__":
    ROWS = 50
    WIDTH = 800
    WINDOW = pg.display.set_mode((WIDTH, WIDTH))

    main(WINDOW, ROWS, WIDTH)