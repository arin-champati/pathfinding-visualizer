import board as b
from config import Colors
import pygame as pg
from button import create_button

def __create_dropdown(dropdown, entries):
    results = []
    for entry in entries:
        pass

def __alg_bar(window, dropdown, a_star, dijkstra, width, height):

    # return true if button is not pressed
    def ret_true():
        return True

    # return false so that start screen exits
    def ret_false():
        return False

    # starting coordinates of dropdown menu
    x = 0
    w = width / 5 - 0.5
    y = 0
    h = height - width

    # Static button
    if dropdown == False:
        dropdown = create_button(window, lambda: ret_false(), lambda: ret_true(), 
        width/48, "Algorithms", Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, y, w, h)
        render_h = h

    # Dropdown view
    elif dropdown == True:
        dropdown = create_button(window, lambda: ret_true(), lambda: ret_false(), 
        width/48, "Algorithms", Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, y, w, h)
        
        y += h
        a_star = create_button(window, lambda: ret_false(), lambda: ret_true(), 
        width/48, "A Star", Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, y, w, h)
        
        y += h
        dijkstra = create_button(window, lambda: ret_false(), lambda: ret_true(), 
        width/48, "Dijkstra", Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, y, w, h)
        render_h = y
    
    # Special case
    if a_star or dijkstra == True:
        dropdown = create_button(window, lambda: ret_false(), lambda: ret_true(), 
        width/48, "Algorithms", Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, 0, w, h)

    #pg.display.update(x, y, w, render_h)
    pg.time.Clock().tick(120)

    return dropdown, a_star, dijkstra

def __metric_bar(window, dropdown, distance, time, width, height):

    # return true if button is not pressed
    def ret_true():
        return True

    # return false so that start screen exits
    def ret_false():
        return False

    # starting coordinates of dropdown menu
    x = width / 5 + 0.5
    w = width / 5
    y = 0
    h = height - width

    # Static button
    if dropdown == False:
        dropdown = create_button(window, lambda: ret_false(), lambda: ret_true(), 
        width/48, "Metrics", Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, y, w, h)
        render_h = h

    # Dropdown view
    elif dropdown == True:
        dropdown = create_button(window, lambda: ret_true(), lambda: ret_false(), 
        width/48, "Metrics", Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, y, w, h)
        
        y += h
        distance = create_button(window, lambda: ret_false(), lambda: ret_true(), 
        width/48, "Distance", Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, y, w, h)
        
        y += h
        time = create_button(window, lambda: ret_false(), lambda: ret_true(), 
        width/48, "Time", Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, y, w, h)
        render_h = y
    
    # Special case
    if distance or time == True:
        dropdown = create_button(window, lambda: ret_false(), lambda: ret_true(), 
        width/48, "Metrics", Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, 0, w, h)

    #pg.display.update(x, y, w, render_h)
    pg.time.Clock().tick(120)

    return dropdown, distance, time

def __board_bar(window, dropdown, new, erase, reset, width, height):

    # return true if button is not pressed
    def ret_true():
        return True

    # return false so that start screen exits
    def ret_false():
        return False

    # starting coordinates of dropdown menu
    x = (width / 5 + 0.5) * 2
    w = width / 5 - 1
    y = 0
    h = height - width

    # Static button
    if dropdown == False:
        dropdown = create_button(window, lambda: ret_false(), lambda: ret_true(), 
        width/48, "Board", Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, y, w, h)
        render_h = h

    # Dropdown view
    elif dropdown == True:
        dropdown = create_button(window, lambda: ret_true(), lambda: ret_false(), 
        width/48, "Board", Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, y, w, h)
        
        y += h
        new = create_button(window, lambda: ret_false(), lambda: ret_true(), 
        width/48, "New", Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, y, w, h)
        
        y += h
        erase = create_button(window, lambda: ret_false(), lambda: ret_true(), 
        width/48, "Erase", Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, y, w, h)

        y += h
        reset = create_button(window, lambda: ret_false(), lambda: ret_true(), 
        width/48, "Reset", Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, y, w, h)
        render_h = y
    
    # Special case
    if new or erase or reset == True:
        dropdown = create_button(window, lambda: ret_false(), lambda: ret_true(), 
        width/48, "Board", Colors.LIGHTER_BLUE, Colors.DARK_BLUE, x, 0, w, h)

    #pg.display.update(x, y, w, render_h)
    pg.time.Clock().tick(120)

    return dropdown, new, erase, reset

def result(window, time, distance, width, height):
    # starting coordinates of dropdown menu
    x = (width / 5) * 3 + 1
    w = width / 5 
    y = 0
    h = height - width
    """
    if not(time and distance):
        # Static button
        create_button(window, lambda: "", lambda: "", 
        width/48, f"", Colors.DARK_BLUE, Colors.DARK_BLUE, x, y, w, h)

    else:
    """
    time = round(time, 3)
    distance = round(distance, 0)

    # Static button
    create_button(window, lambda: "", lambda: "", 
    width/72, f"Time: {time}, Distance: {distance}", Colors.DARK_BLUE, Colors.DARK_BLUE, x, y, w, h)

    return time, distance

def menu(window, dropdown_alg, a_star, dijkstra, dropdown_metric, distance_metric, time_metric, dropdown_board, new, erase, reset, time, distance, width, height): 
    time, distance = result(window, time, distance, width, height)
    
    # If alg dropdown pressed then other
    if dropdown_alg == True and (dropdown_metric == False and dropdown_board == False):
        # Only allow one dropdown menu to be open at once
        dropdown_alg, a_star, dijkstra = __alg_bar(window, dropdown_alg, a_star, dijkstra, width, height)
        dropdown_metric, distance_metric, time_metric = __metric_bar(window, dropdown_metric, distance_metric, time_metric, width, height)
        dropdown_board, new, erase, reset = __board_bar(window, dropdown_board, new, erase, reset, width, height)
        if dropdown_metric == True or dropdown_board == True:
            dropdown_alg = False
    
    # If metric dropdown pressed then other
    elif dropdown_metric == True and (dropdown_alg == False and dropdown_board == False):
        dropdown_alg, a_star, dijkstra = __alg_bar(window, dropdown_alg, a_star, dijkstra, width, height)
        dropdown_metric, distance_metric, time_metric = __metric_bar(window, dropdown_metric, distance_metric, time_metric, width, height)
        dropdown_board, new, erase, reset = __board_bar(window, dropdown_board, new, erase, reset, width, height)
        if dropdown_alg == True or dropdown_board == True:
            dropdown_metric = False

    # If board dropdown pressed then other
    elif dropdown_board == True and (dropdown_metric == False and dropdown_alg == False):
        dropdown_alg, a_star, dijkstra = __alg_bar(window, dropdown_alg, a_star, dijkstra, width, height)
        dropdown_metric, distance_metric, time_metric = __metric_bar(window, dropdown_metric, distance_metric, time_metric, width, height)
        dropdown_board, new, erase, reset = __board_bar(window, dropdown_board, new, erase, reset, width, height)
        if dropdown_alg == True or dropdown_metric == True:
            dropdown_board = False

    else:
        dropdown_alg, a_star, dijkstra = __alg_bar(window, dropdown_alg, a_star, dijkstra, width, height)
        dropdown_metric, distance_metric, time_metric = __metric_bar(window, dropdown_metric, distance_metric, time_metric, width, height)
        dropdown_board, new, erase, reset = __board_bar(window, dropdown_board, new, erase, reset, width, height)
     
    return dropdown_alg, a_star, dijkstra, dropdown_metric, distance_metric, time_metric, dropdown_board, new, erase, reset, time, distance