import board as b
import config
from copy import deepcopy

def new_board(rows, width, height):
    ALG_FINISHED = False

    board = b.initialize_board(rows, width, height)
    old_board = deepcopy(board)

    # STATUS variables
    ALG_STARTED = False

    start_node = None
    end_node = None

    return False, ALG_STARTED, ALG_FINISHED, board, old_board, start_node, end_node

def erase_board(old_board):
    ALG_FINISHED = False
    board = deepcopy(old_board)

    # STATUS variables
    ALG_STARTED = False

    start_node = None
    end_node = None

    return False, ALG_STARTED, ALG_FINISHED, board, old_board, start_node, end_node

def reset_board(alg_started, alg_finished, board, boundary_board, start_node, end_node):
    if boundary_board is not None and start_node is not None and end_node is not None:
        ALG_FINISHED = False

        row1, col1 = start_node.position()
        row2, col2 = end_node.position()

        board = deepcopy(boundary_board)

        start_node = board[row1][col1]
        end_node = board[row2][col2]

        start_node.make_start()
        end_node.make_end()

        boundary_board = None

        # STATUS variables
        RUNNING = True
        ALG_STARTED = False
        return False, ALG_STARTED, ALG_FINISHED, board, boundary_board, start_node, end_node

    else:
        return False, alg_started, alg_finished, board, boundary_board, start_node, end_node
