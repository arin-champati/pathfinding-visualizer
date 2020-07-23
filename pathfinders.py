from queue import PriorityQueue
import pygame as pg
import board
from board import Node
from functools import partial
import math
from copy import deepcopy
from config import Speeds

# manhattan heuristic
def manhattan(node_1, node_2, width):
    point_1 = node_1.position()
    point_2 = node_2.position()
    x1, y1 = point_1
    x2, y2 = point_2

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return (dx + dy) * (1 + 1/(width*width))

# time heuristic
def time(node_1, node_2, width):
    point_1 = node_1.position()
    point_2 = node_2.position()
    x1, y1 = point_1
    x2, y2 = point_2

    # find euclidean distance
    dx = (x1 - x2)
    dx *=dx
    dy = (y1 - y2)
    dy *=dy

    distance = dx + dy

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    max_speed = max(Speeds.HIGHWAY_SPEED, Speeds.LOCAL_SPEED)
    avg_speed = (Speeds.HIGHWAY_SPEED + Speeds.LOCAL_SPEED) / 2

    # break ties as well
    return (distance / avg_speed) * (1 + ((1/ max_speed) / (width * width)))

# once path is found, use this to find shortest
def reconstruct_path(start_node, current, draw_path):
    speed = 0
    distance = 0

    while (current.parent != start_node):
        current = current.parent
        current.make_path()
        speed += current.speed
        distance += 1
        
    print(f"Time: {distance / speed}, Distance: {distance}")
    
    draw_path()

# all of these functions will take in as the first argument
# an ambiguous function named draw(), which updates the window
def a_star(draw_path, start_node, end_node, width, heuristic):
    index = 0
    if heuristic == "time":
        function1 = partial(time, start_node, end_node, width)
    elif heuristic == "distance":
        function1 = partial(manhattan, start_node, end_node, width)
    
    # min priority queue to get node with min f constant time
    open_list = PriorityQueue()
    # tradeoff with memory for time - keep track of open nodes
    open_list_tracker = {start_node}

    # initialize node values
    open_list.put((0, index, start_node))
    start_node.f = function1()
    start_node.g = 0

    while not open_list.empty():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        current = open_list.get()[2]
        open_list_tracker.remove(current)

        # if we have found the destination, render the path
        if current == end_node:
            reconstruct_path(start_node, end_node, draw_path)
            end_node.make_end()
            return True

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
                    function2 = partial(time, neighbor, end_node, width)
                elif heuristic is "distance":
                    function2 = partial(manhattan, neighbor, end_node, width)

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

        draw_path()

        if current != start_node:
            current.make_closed()

    return False