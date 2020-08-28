import pygame as pg
import board as b
from config import Colors
from button import create_button
import numpy as np

def __create_dropdown(window, button_event, entries, width, x, y, w, h):
    """
    window: (window) pygame window
    button_event: (pygame event) pygame event that is either MOUSEBUTTONDOWN or MOUSEBUTTON UP
    entries: (list) list of entries for dropdown menu in order from top to bottom
    width: (int) 
    x: (int) pixel x value of button
    y: (int) pixel y value of button
    w: (int) pixel width of button
    h: (int) pixel height of button

    output: results (array) array of same dimensions as entries, with updated values
    summary: handles the dropdown menu functionality. Updates the inputed entries according
    to user input (i.e. mouse being pressed)
    """
    results = []
    selected = False
    prev_true = None

    for i, entry in enumerate(entries):
        results.append(entry[1])
        if entry[1] == True:
            prev_true = i

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
        result = create_button(window, button_event, lambda: ret_false(), lambda: ret_true(), 
        width/54, name, Colors.BUTTON_HOVER, Colors.BUTTON_DEFAULT, x, y, w, h)

        results[0] = result

    # Dropdown view
    elif dropdown == True:
        name = entries[0][0]
        result = create_button(window, button_event, lambda: ret_true(), lambda: ret_false(), 
        width/54, name, Colors.BUTTON_HOVER, Colors.BUTTON_DEFAULT, x, y, w, h) 

        results[0] = result       

        for i, entry in enumerate(entries[1:]):
            y += h
            name = entry[0]
            result = create_button(window, button_event, lambda: ret_false(), lambda: ret_true(), 
            width/54, name, Colors.BUTTON_HOVER, Colors.BUTTON_DEFAULT, x, y, w, h)

            results[i + 1] = result

            # if something is selected, mark it down
            if result == True:
                selected = True
                

    # if something has been selected, stop showing menu
    if selected == True:
        name = entries[0][0]
        result = create_button(window, button_event, lambda: ret_false(), lambda: ret_true(), 
        width/54, name, Colors.BUTTON_HOVER, Colors.BUTTON_DEFAULT, x, 0, w, h)

        results[0] = result
    
    # if nothing has been selected, return to the previous state
    elif prev_true is not None and prev_true != 0:
        results[prev_true] = True

    return results
        
def __alg_bar(window, button_event, dropdown, a_star, dijkstra, bfs, dfs, width, height):
    """
    window: (window) pygame window
    button_event: (pygame event) pygame event that is either MOUSEBUTTONDOWN or MOUSEBUTTON UP
    dropdown: (boolean) true if alg bar dropdown is being rendered
    a_star: (boolean) true if a_star algorithm has been selected
    dijkstra: (boolean) true if dijkstra's algorithm has been selected
    bfs: (boolean) true if bfs has been selected
    dfs: (boolean) true if dfs has been selected
    width: (int) width of window in pixels
    height: (int) height of window in pixels

    output: (booleans) updataed boolean results (dropdown, a_star, dijkstra, bfs, dfs)
    summary: client for __create_dropdown. creates dropdown and updates the values
    """
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

    results = __create_dropdown(window, button_event, entries, width, x, y, w, h)

    return results[0], results[1], results[2], results[3], results[4]
    

def __metric_bar(window, button_event, dropdown, distance, time, width, height):
    """
    window: (window) pygame window
    button_event: (pygame event) pygame event that is either MOUSEBUTTONDOWN or MOUSEBUTTON UP
    dropdown: (boolean) true if metric bar dropdown is being rendered
    distance: (boolean) true if distance metric has been selected
    time: (boolean) true if time metric has been selected
    width: (int) width of window in pixels
    height: (int) height of window in pixels

    output: (booleans) updataed boolean results (dropdown, distance, time)
    summary: client for __create_dropdown. creates dropdown and updates the values
    """
    # starting coordinates of dropdown menu
    x = width / 5 + 1
    w = width / 5 - 1
    y = 0
    h = height - width

    metric_entry = ["Metrics", dropdown]
    distance_entry = ["Distance", distance]
    time_entry = ["Time", time]

    entries = [metric_entry, distance_entry, time_entry]

    results = __create_dropdown(window, button_event, entries, width, x, y, w, h)

    return results[0], results[1], results[2]

def __board_bar(window, button_event, dropdown, new, erase, reset, width, height):
    """
    window: (window) pygame window
    button_event: (pygame event) pygame event that is either MOUSEBUTTONDOWN or MOUSEBUTTON UP
    dropdown: (boolean) true if board bar dropdown is being rendered
    new: (boolean) true if new board has been selected
    erase: (boolean) true if erase board has been selected
    reset: (boolean) true if reset board has been selected
    width: (int) width of window in pixels
    height: (int) height of window in pixels

    output: (booleans) updataed boolean results (dropdown, new, erase, reset)
    summary: client for __create_dropdown. creates dropdown and updates the values
    """
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

    results = __create_dropdown(window, button_event, entries, width, x, y, w, h)

    return results[0], results[1], results[2], results[3]


def time_result(window, button_event, time, width, height):
    """
    window: (window) pygame window
    button_event: (pygame event) pygame event that is either MOUSEBUTTONDOWN or MOUSEBUTTON UP
    time: (float) the path's time, based off the speed of the nodes and distance of the path
    width: (int) width of window in pixels
    height: (int) height of window in pixels

    output: (int) updataed time
    summary: creates a static button and updates the time displayed on the button
    """
    # starting coordinates of dropdown menu
    x = (width / 5) * 3 + 1
    w = width / 5 - 1
    y = 0
    h = height - width

    time = round(time, 2)

    # Static button
    create_button(window, button_event, lambda: "", lambda: "", 
    width/54, f"Time: {time}", Colors.BUTTON_DEFAULT, Colors.BUTTON_DEFAULT, x, y, w, h)

    return time

def distance_result(window, button_event, distance, width, height):
    """
    window: (window) pygame window
    button_event: (pygame event) pygame event that is either MOUSEBUTTONDOWN or MOUSEBUTTON UP
    distance: (float) the path's distance
    width: (int) width of window in pixels
    height: (int) height of window in pixels

    output: (int) updataed distance
    summary: creates a static button and updates the distance displayed on the button
    """
    # starting coordinates of dropdown menu
    x = (width / 5) * 4 + 1
    w = width /5
    y = 0
    h = height - width

    distance = round(distance, 0)

    # Static button
    create_button(window, button_event, lambda: "", lambda: "", 
    width/54, f"Distance: {distance}", Colors.BUTTON_DEFAULT, Colors.BUTTON_DEFAULT, x, y, w, h)

    return distance

def menu(window, button_event, dropdown_alg, a_star, dijkstra, bfs, dfs, dropdown_metric, distance_metric, time_metric, dropdown_board, new, erase, reset, time, distance, width, height): 
    """
    window: (window) pygame window
    button_event: (pygame event) pygame event that is either MOUSEBUTTONDOWN or MOUSEBUTTON UP
    dropdown_alg: (boolean) true if alg bar dropdown is being rendered
    a_star: (boolean) true if a_star algorithm has been selected
    dijkstra: (boolean) true if dijkstra's algorithm has been selected
    bfs: (boolean) true if bfs has been selected
    dfs: (boolean) true if dfs has been selected

    dropdown_metric: (boolean) true if metric bar dropdown is being rendered
    distance_metric: (boolean) true if distance metric has been selected
    time_metric: (boolean) true if time metric has been selected

    dropdown_board: (boolean) true if board bar dropdown is being rendered
    new: (boolean) true if new board has been selected
    erase: (boolean) true if erase board has been selected
    reset: (boolean) true if reset board has been selected

    time: (float) the path's time, based off the speed of the nodes and distance of the path
    distance: (float) the path's distance

    width: (int) width of window in pixels
    height: (int) height of window in pixels

    output: (booleans) updataed boolean results (dropdown_alg, a_star, dijkstra, bfs, dfs, dropdown_metric, distance_metric, 
    time_metric, dropdown_board, new, erase, reset, time, distance)

    summary: client for every function in this module. Creates the navigation bar that includes the algorithm dropdown, metric
    dropdown, board dropdown, time button, and distance button. It updates every one of these values based off user input
    and input status variables. 
    """
    
    time = time_result(window, button_event, time, width, height)
    distance = distance_result(window, button_event, distance, width, height)
    
    # If alg dropdown pressed then other
    if dropdown_alg == True and (dropdown_metric == False and dropdown_board == False):
        dropdown_alg, a_star, dijkstra, bfs, dfs = __alg_bar(window, button_event, dropdown_alg, a_star, dijkstra, bfs, dfs, width, height)
        dropdown_metric, distance_metric, time_metric = __metric_bar(window, button_event, dropdown_metric, distance_metric, time_metric, width, height)
        dropdown_board, new, erase, reset = __board_bar(window, button_event, dropdown_board, new, erase, reset, width, height)
        # Only allow one dropdown menu to be open at once
        if dropdown_metric == True or dropdown_board == True:
            dropdown_alg = False
    
    # If metric dropdown pressed then other
    elif dropdown_metric == True and (dropdown_alg == False and dropdown_board == False):
        dropdown_alg, a_star, dijkstra, bfs, dfs = __alg_bar(window, button_event, dropdown_alg, a_star, dijkstra, bfs, dfs, width, height)
        dropdown_metric, distance_metric, time_metric = __metric_bar(window, button_event, dropdown_metric, distance_metric, time_metric, width, height)
        dropdown_board, new, erase, reset = __board_bar(window, button_event, dropdown_board, new, erase, reset, width, height)
        if dropdown_alg == True or dropdown_board == True:
            dropdown_metric = False

    # If board dropdown pressed then other
    elif dropdown_board == True and (dropdown_metric == False and dropdown_alg == False):
        dropdown_alg, a_star, dijkstra, bfs, dfs = __alg_bar(window, button_event, dropdown_alg, a_star, dijkstra, bfs, dfs, width, height)
        dropdown_metric, distance_metric, time_metric = __metric_bar(window, button_event, dropdown_metric, distance_metric, time_metric, width, height)
        dropdown_board, new, erase, reset = __board_bar(window, button_event, dropdown_board, new, erase, reset, width, height)
        if dropdown_alg == True or dropdown_metric == True:
            dropdown_board = False
    else:
        dropdown_alg, a_star, dijkstra, bfs, dfs = __alg_bar(window, button_event, dropdown_alg, a_star, dijkstra, bfs, dfs, width, height)
        dropdown_metric, distance_metric, time_metric = __metric_bar(window, button_event, dropdown_metric, distance_metric, time_metric, width, height)
        dropdown_board, new, erase, reset = __board_bar(window, button_event, dropdown_board, new, erase, reset, width, height)
    
    return dropdown_alg, a_star, dijkstra, bfs, dfs, dropdown_metric, distance_metric, time_metric, dropdown_board, new, erase, reset, time, distance