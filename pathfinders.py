import pygame as pg
import board as b
from board import Node
from config import Speeds, AlgorithmRender
from nav_bar import menu

from queue import PriorityQueue, Queue
from functools import partial
import math
from copy import deepcopy

# if alg is running, these functionalities should be allowed
def __functionalities():
    """
    summary: loops through pygame events and quits the program when q is pressed
    or the x button
    """
    for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if  event.key == pg.K_q:
                    pg.quit()
                    quit()

def __update_neighbors(board):
    """
    board: (list) list of lists of nodes

    summary: updates the neighbors of every node in the board
    """
    for row in board:
        for node in row:
            node.update_neighbors(board) 
    
# manhattan heuristic
def __manhattan(node_1, node_2, length):
    """
    node_1: (node) from node
    node_2: (node) to node
    length: (int) length of one node in pixels

    output: (int) manhattan distance normalized by length of one step/max expected length
    to break ties
    summary: calculates manhattan distance between two nodes.
    """
    point_1 = node_1.position()
    point_2 = node_2.position()
    x1, y1 = point_1
    x2, y2 = point_2

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    return (dx + dy) * (1 + (1 / (length*length)))

# time heuristic
def __time(node_1, node_2, length):
    """
    node_1: (node) from node
    node_2: (node) to node
    length: (int) length of one node in pixels

    output: (int) time from 'from' node to 'to' node normalized by time of one step/max expected time
    summary: calculates time between two nodes.
    """    
    point_1 = node_1.position()
    point_2 = node_2.position()
    x1, y1 = point_1
    x2, y2 = point_2

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    distance = dx + dy

    min_speed = min(Speeds.HIGHWAY_SPEED, Speeds.LOCAL_SPEED)
    max_speed = max(Speeds.HIGHWAY_SPEED, Speeds.LOCAL_SPEED)
    avg_speed = (Speeds.HIGHWAY_SPEED + Speeds.LOCAL_SPEED) / 2

    # break ties as well
    return (distance / avg_speed) * (1 + ((1 / avg_speed) / (length*length / min_speed)))


# once path is found, use this to find shortest
def reconstruct_path(start_node, end_node, draw_path, rows):
    """
    start_node: (node) beginning query of path
    end_node: (node) end query of path
    draw_path: function that renders the path
    rows: (int) amount of rows on board

    output: (float, float) time and distance it takes to get from start_node to end_node
    summary: draws the calculated shortest path from start_node to end_node and returns
    the time and distance it takes to get there
    """
    speed = start_node.speed
    distance = 1
    current = end_node

    while (current.parent != start_node):
        __functionalities()
        
        current = current.parent
        current.make_path()
        speed += current.speed
        distance += 1
    
    draw_path()
    return (distance / (speed / distance)) * 100, distance

# all of these functions will take in as the first argument
# an ambiguous function named draw(), which updates the window
def a_star(window, draw_path, draw_menu, board, start_node, end_node, rows, width, height, heuristic):
    """
    window: (window) pygame window
    draw_path: (function) function that draws path after it has been found
    draw_menu: (function) function that renders the menu
    board: (list of lists) N x N list of lists of nodes
    start_node: (node) beginning query of path
    end_node: (node) end query of path
    rows: (int) amount of rows on board
    width: (int) pixel width of board
    height: (int) pixel height of board
    heuristic: (string) either time or distance - heuristic that algorithm uses to find shortest path

    output: True (alg_finished state), time, distance
    summary: runs a star algorithm with either time or distance heuristic. Renders the open and closed
    sets as the algorithm is running as well as the shortest path when it is finished.
    """
    __update_neighbors(board)

    index = 0
    length = width // rows

    if heuristic == "time":
        function1 = partial(__time, start_node, end_node, length)
    elif heuristic == "distance":
        function1 = partial(__manhattan, start_node, end_node, length)
    
    # min priority queue to get node with min f constant time
    open_list = PriorityQueue()
    # tradeoff with memory for time - keep track of open nodes
    open_list_tracker = {start_node}

    # initialize node values
    start_node.g = 0
    open_list.put((start_node.g, index, start_node))
    start_node.f = function1()

    while not open_list.empty():
        __functionalities()

        unrendered_neighbors = []

        current = open_list.get()[2]
        open_list_tracker.remove(current)

        # if we have found the destination, render the path
        if current == end_node:
            time, distance = reconstruct_path(start_node, end_node, draw_path, rows)
            end_node.make_end()
            return True, time, distance

        # check all of the neighbors and see if there are any
        # shorter paths to those neighbors
        for neighbor in current.neighbors:
            if heuristic is "time":
                temp_g_score = current.g + current.time() # cost is time
            elif heuristic is "distance":
                temp_g_score = current.g + 1

            # if this g score is better than the previous one
            # update the results
            if temp_g_score < neighbor.g:
                if heuristic is "time":
                    function2 = partial(__time, neighbor, end_node, length)
                elif heuristic is "distance":
                    function2 = partial(__manhattan, neighbor, end_node, length)

                neighbor.parent = current
                neighbor.g = temp_g_score
                neighbor.f = temp_g_score + function2()
                # add the neighbor to the open list
                if neighbor not in open_list_tracker:
                    index += 1
                    open_list.put((neighbor.f, index, neighbor))
                    open_list_tracker.add(neighbor)
                    # don't color the end node
                    if neighbor != end_node:
                        neighbor.make_open()
            
            # only render the nodes that haven't been changed
            if neighbor.is_rendered() == False:
                unrendered_neighbors.append(neighbor)

        pg.time.Clock().tick(AlgorithmRender.A_STAR_RENDER)
        b.draw_node(window, draw_menu, board, unrendered_neighbors, rows, width, height)

        if current != start_node:
            current.make_closed()

    return True, 0, 0


def dijkstra(window, draw_path, draw_menu, board, start_node, end_node, rows, width, height, heuristic):
    """
    window: (window) pygame window
    draw_path: (function) function that draws path after it has been found
    draw_menu: (function) function that renders the menu
    board: (list of lists) N x N list of lists of nodes
    start_node: (node) beginning query of path
    end_node: (node) end query of path
    rows: (int) amount of rows on board
    width: (int) pixel width of board
    height: (int) pixel height of board
    heuristic: (string) either time or distance - heuristic that algorithm uses to find shortest path

    output: True (alg_finished state), time, distance
    summary: runs dijkstra's algorithm with either time or distance heuristic. Renders the open and closed
    sets as the algorithm is running as well as the shortest path when it is finished.
    """
    __update_neighbors(board)

    index = 0
    
    # min priority queue to get node with min f constant time
    open_list = PriorityQueue()
    # tradeoff with memory for time - keep track of open nodes
    open_list_tracker = {start_node}

    # initialize node values
    start_node.f = 0
    open_list.put((start_node.f, index, start_node))

    while not open_list.empty():
        __functionalities()

        unrendered_neighbors = []

        current = open_list.get()[2]
        open_list_tracker.remove(current)

        # if we have found the destination, render the path
        if current == end_node:
            time, distance = reconstruct_path(start_node, end_node, draw_path, rows)
            end_node.make_end()
            return True, time, distance

        # check all of the neighbors and see if there are any
        # shorter paths to those neighbors
        for neighbor in current.neighbors:
            if heuristic is "time":
                temp_f_score = current.f + current.time() # cost is time
            elif heuristic is "distance":
                temp_f_score = current.f + 1

            # if this g score is better than the previous one
            # update the results
            if temp_f_score < neighbor.f:
                neighbor.parent = current
                neighbor.f = temp_f_score

                # add the neighbor to the open list
                if neighbor not in open_list_tracker:
                    index += 1
                    open_list.put((neighbor.f, index, neighbor))
                    open_list_tracker.add(neighbor)
                    # don't color the end node
                    if neighbor != end_node:
                        neighbor.make_open()

            # only render the nodes that haven't been changed
            if neighbor.is_rendered() == False:
                unrendered_neighbors.append(neighbor)
        
        pg.time.Clock().tick(AlgorithmRender.DIJKSATRA_RENDER)
        b.draw_node(window, draw_menu, board, unrendered_neighbors, rows, width, height)

        if current != start_node:
            current.make_closed()

    return True, 0, 0

def bfs(window, draw_path, draw_menu, board, start_node, end_node, rows, width, height):
    """
    window: (window) pygame window
    draw_path: (function) function that draws path after it has been found
    draw_menu: (function) function that renders the menu
    board: (list of lists) N x N list of lists of nodes
    start_node: (node) beginning query of path
    end_node: (node) end query of path
    rows: (int) amount of rows on board
    width: (int) pixel width of board
    height: (int) pixel height of board

    output: True (alg_finished state), time, distance
    summary: runs bfs algorithm. Renders the open and closed
    sets as the algorithm is running as well as the shortest path when it is finished.
    """

    __update_neighbors(board)

    open_list = Queue()
    open_list.put(start_node)

    while not open_list.empty():
        __functionalities()

        unrendered_neighbors = []
        
        current = open_list.get()

        # if we have found the destination, render the path
        if current == end_node:
            time, distance = reconstruct_path(start_node, end_node, draw_path, rows)
            end_node.make_end()
            return True, time, distance

        for neighbor in current.neighbors:
            if not neighbor.parent:
                neighbor.parent = current
                open_list.put(neighbor)
                # don't color the end node
                if neighbor != (end_node and start_node):
                    neighbor.make_open()

            # only render the nodes that haven't been changed
            if neighbor.is_rendered() == False:
                unrendered_neighbors.append(neighbor)
        
        pg.time.Clock().tick(AlgorithmRender.BFS_RENDER)
        b.draw_node(window, draw_menu, board, unrendered_neighbors, rows, width, height)

        if current != start_node:
            current.make_closed()

    return True, 0, 0

def __dfs_helper(window, draw_path, draw_menu, board, visited, unrendered_neighbors, current, start_node, end_node, rows, width, height):
    """
    window: (window) pygame window
    draw_path: (function) function that draws path after it has been found
    draw_menu: (function) function that renders the menu
    board: (list of lists) N x N list of lists of nodes
    visited: (list) nodes that have been visited by algorithm
    unrendered_neighbors: (list) list of the unrendered neighbors of current node
    current: (node) current node
    start_node: (node) beginning query of path
    end_node: (node) end query of path
    rows: (int) amount of rows on board
    width: (int) pixel width of board
    height: (int) pixel height of board

    output: (boolean) if algorithm has found path 
    summary: runs dfs on the board and stops once path is found
    """
    __functionalities()

    if current not in visited:
        if current == end_node:
            return True

        visited.add(current)

        for neighbor in current.neighbors:
            if not neighbor.parent:
                neighbor.parent = current
                # don't color the end node
                if neighbor != (end_node and start_node):
                    neighbor.make_closed()
                
                # only render the nodes that haven't been changed
                if neighbor.is_rendered() == False:
                    unrendered_neighbors.append(neighbor)
            
                pg.time.Clock().tick(AlgorithmRender.DFS_RENDER)
                b.draw_node(window, draw_menu, board, unrendered_neighbors, rows, width, height)

                if __dfs_helper(window, draw_path, draw_menu, board, visited, unrendered_neighbors, neighbor, start_node, end_node, rows, width, height):
                    return True            

    return False

def dfs(window, draw_path, draw_menu, board, start_node, end_node, rows, width, height):
    """
    window: (window) pygame window
    draw_path: (function) function that draws path after it has been found
    draw_menu: (function) function that renders the menu
    board: (list of lists) N x N list of lists of nodes
    start_node: (node) beginning query of path
    end_node: (node) end query of path
    rows: (int) amount of rows on board
    width: (int) pixel width of board
    height: (int) pixel height of board

    output: True (alg_finished state), time, distance
    summary: runs dfs algorithm. Renders the visited set as the algorithm is running 
    as well as the shortest path when it is finished.
    """

    __update_neighbors(board)
    visited = set()
    unrendered_neighbors = []
    time = 0
    distance = 0
    
    if __dfs_helper(window, draw_path, draw_menu, board, visited, unrendered_neighbors, start_node, start_node, end_node, rows, width, height):
        time, distance = reconstruct_path(start_node, end_node, draw_path, rows)
        end_node.make_end()

    return True, time, distance