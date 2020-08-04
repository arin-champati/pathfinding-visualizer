import board as b
import board as b
from config import Colors
import pygame as pg
from button import create_button
import numpy as np

def __create_dropdown(window, event, entries, width, x, y, w, h):
    
    num_entries = len(entries)
    selected = False
    results = []

    for entry in entries:
        results.append(entry[1])

    # return true if button is not pressed
    def ret_true():
        return True

    # return false so that start screen exits
    def ret_false():
        return False

    dropdown = entries[0][1]

    # Static button
    if dropdown == False:
        name = entries[0][0]
        result = create_button(window, event, lambda: ret_false(), lambda: ret_true(), 
        width/54, name, Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, y, w, h)

        results[0] = result

    # Dropdown view
    elif dropdown == True:
        name = entries[0][0]
        result = create_button(window, event, lambda: ret_true(), lambda: ret_false(), 
        width/54, name, Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, y, w, h) 

        results[0] = result       

        for i, entry in enumerate(entries[1:]):
            y += h
            name = entry[0]
            result = create_button(window, event, lambda: ret_false(), lambda: ret_true(), 
            width/54, name, Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, y, w, h)

            results[i + 1] = result

            # if something is selected, mark it down
            if result == True:
                selected = True
                

    # Special case
    if selected == True:
        name = entries[0][0]
        result = create_button(window, event, lambda: ret_false(), lambda: ret_true(), 
        width/54, name, Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, 0, w, h)

        results[0] = result

    return results
        
def __alg_bar(window, event, dropdown, a_star, dijkstra, bfs, dfs, width, height):
    # starting coordinates of dropdown menu
    x = 0
    w = width / 5
    y = 0
    h = height - width

    alg_entry = ["Algorithm", dropdown]
    a_star_entry = ["A Star", a_star]
    dijkstra_entry = ["Dijkstra", dijkstra]
    bfs_entry = ["BFS", bfs]
    dfs_entry = ["DFS", dfs]

    entries = [alg_entry, a_star_entry, dijkstra_entry, bfs_entry, dfs_entry]

    results = __create_dropdown(window, event, entries, width, x, y, w, h)

    return results[0], results[1], results[2], results[3], results[4]
    

def __metric_bar(window, event, dropdown, distance, time, width, height):
    # starting coordinates of dropdown menu
    x = width / 5 + 1
    w = width / 5 - 1
    y = 0
    h = height - width

    metric_entry = ["Metrics", dropdown]
    distance_entry = ["Distance", distance]
    time_entry = ["Time", time]

    entries = [metric_entry, distance_entry, time_entry]

    results = __create_dropdown(window, event, entries, width, x, y, w, h)

    return results[0], results[1], results[2]

def __board_bar(window, event, dropdown, new, erase, reset, width, height):
    # starting coordinates of dropdown menu
    x = (width / 5) * 2 + 1
    w = width / 5 - 1
    y = 0
    h = height - width

    board_entry = ["Board", dropdown]
    new_entry = ["New", new]
    erase_entry = ["Erase", erase]
    reset_entry = ["Reset", reset]

    entries = [board_entry, new_entry, erase_entry, reset_entry]

    results = __create_dropdown(window, event, entries, width, x, y, w, h)

    return results[0], results[1], results[2], results[3]


def time_result(window, event, time, width, height):
    # starting coordinates of dropdown menu
    x = (width / 5) * 3 + 1
    w = width / 5 - 1
    y = 0
    h = height - width
    """
    if not(time and distance):
        # Static button
        create_button(window, lambda: "", lambda: "", 
        width/54, f"", Colors.DARK_BLUE, Colors.DARK_BLUE, x, y, w, h)

    else:
    """
    time = round(time, 2)

    # Static button
    create_button(window, event, lambda: "", lambda: "", 
    width/54, f"Time: {time}", Colors.DARK_BLUE, Colors.DARK_BLUE, x, y, w, h)

    return time

def distance_result(window, event, distance, width, height):
    # starting coordinates of dropdown menu
    x = (width / 5) * 4 + 1
    w = width /5
    y = 0
    h = height - width
    """
    if not(time and distance):
        # Static button
        create_button(window, lambda: "", lambda: "", 
        width/54, f"", Colors.DARK_BLUE, Colors.DARK_BLUE, x, y, w, h)

    else:
    """
    distance = round(distance, 0)

    # Static button
    create_button(window, event, lambda: "", lambda: "", 
    width/54, f"Distance: {distance}", Colors.DARK_BLUE, Colors.DARK_BLUE, x, y, w, h)

    return distance

def menu(window, event, dropdown_alg, a_star, dijkstra, bfs, dfs, dropdown_metric, distance_metric, time_metric, dropdown_board, new, erase, reset, time, distance, width, height): 
    
    time = time_result(window, event, time, width, height)
    distance = distance_result(window, event, distance, width, height)
    
    # If alg dropdown pressed then other
    if dropdown_alg == True and (dropdown_metric == False and dropdown_board == False):
        dropdown_alg, a_star, dijkstra, bfs, dfs = __alg_bar(window, event, dropdown_alg, a_star, dijkstra, bfs, dfs, width, height)
        dropdown_metric, distance_metric, time_metric = __metric_bar(window, event, dropdown_metric, distance_metric, time_metric, width, height)
        dropdown_board, new, erase, reset = __board_bar(window, event, dropdown_board, new, erase, reset, width, height)
        # Only allow one dropdown menu to be open at once
        if dropdown_metric == True or dropdown_board == True:
            dropdown_alg = False
    
    # If metric dropdown pressed then other
    elif dropdown_metric == True and (dropdown_alg == False and dropdown_board == False):
        dropdown_alg, a_star, dijkstra, bfs, dfs = __alg_bar(window, event, dropdown_alg, a_star, dijkstra, bfs, dfs, width, height)
        dropdown_metric, distance_metric, time_metric = __metric_bar(window, event, dropdown_metric, distance_metric, time_metric, width, height)
        dropdown_board, new, erase, reset = __board_bar(window, event, dropdown_board, new, erase, reset, width, height)
        if dropdown_alg == True or dropdown_board == True:
            dropdown_metric = False

    # If board dropdown pressed then other
    elif dropdown_board == True and (dropdown_metric == False and dropdown_alg == False):
        dropdown_alg, a_star, dijkstra, bfs, dfs = __alg_bar(window, event, dropdown_alg, a_star, dijkstra, bfs, dfs, width, height)
        dropdown_metric, distance_metric, time_metric = __metric_bar(window, event, dropdown_metric, distance_metric, time_metric, width, height)
        dropdown_board, new, erase, reset = __board_bar(window, event, dropdown_board, new, erase, reset, width, height)
        if dropdown_alg == True or dropdown_metric == True:
            dropdown_board = False
    else:
        dropdown_alg, a_star, dijkstra, bfs, dfs = __alg_bar(window, event, dropdown_alg, a_star, dijkstra, bfs, dfs, width, height)
        dropdown_metric, distance_metric, time_metric = __metric_bar(window, event, dropdown_metric, distance_metric, time_metric, width, height)
        dropdown_board, new, erase, reset = __board_bar(window, event, dropdown_board, new, erase, reset, width, height)
    
    return dropdown_alg, a_star, dijkstra, bfs, dfs, dropdown_metric, distance_metric, time_metric, dropdown_board, new, erase, reset, time, distance