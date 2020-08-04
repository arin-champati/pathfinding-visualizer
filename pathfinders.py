from queue import PriorityQueue, Queue
import pygame as pg
import board as b
from board import Node
from functools import partial
import math
from copy import deepcopy
from config import Speeds, AlgorithmRender
from nav_bar import menu

# if alg is running, these functionalities should be allowed
def __functionalities():
    for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if  event.key == pg.K_q:
                    pg.quit()
                    quit()

def __update_neighbors(board):
    # initialize the neighbors for the algorithm
    for row in board:
        for node in row:
            node.update_neighbors(board) 
    
# manhattan heuristic
def __manhattan(node_1, node_2, width):
    point_1 = node_1.position()
    point_2 = node_2.position()
    x1, y1 = point_1
    x2, y2 = point_2

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return (dx + dy) * (1 + 1/(width*width))

# time heuristic
def __time(node_1, node_2, width):
    point_1 = node_1.position()
    point_2 = node_2.position()
    x1, y1 = point_1
    x2, y2 = point_2

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    distance = dx + dy

    min_speed = min(Speeds.HIGHWAY_SPEED, Speeds.LOCAL_SPEED)
    max_speed = max(Speeds.HIGHWAY_SPEED, Speeds.LOCAL_SPEED)
    avg_speed = (Speeds.HIGHWAY_SPEED + Speeds.LOCAL_SPEED + node_1.speed + node_2.speed) / 4

    # break ties as well
    return (distance / avg_speed) * (1 + (1/max_speed) / (width*width))


# once path is found, use this to find shortest
def reconstruct_path(start_node, current, draw_path, rows):
    speed = start_node.speed
    distance = 1

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
    __update_neighbors(board)

    index = 0
    if heuristic == "time":
        function1 = partial(__time, start_node, end_node, width)
    elif heuristic == "distance":
        function1 = partial(__manhattan, start_node, end_node, width)
    
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
                    function2 = partial(__time, neighbor, end_node, width)
                elif heuristic is "distance":
                    function2 = partial(__manhattan, neighbor, end_node, width)

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
    __update_neighbors(board)
    visited = set()
    unrendered_neighbors = []
    time = 0
    distance = 0
    
    if __dfs_helper(window, draw_path, draw_menu, board, visited, unrendered_neighbors, start_node, start_node, end_node, rows, width, height):
        time, distance = reconstruct_path(start_node, end_node, draw_path, rows)
        end_node.make_end()

    return True, time, distance