import board as b
from config import Colors
import pygame as pg
from button import create_button

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

def menu(window, dropdown_alg, a_star, dijkstra, dropdown_metric, distance, time, width, height):
    # Only allow one dropdown menu to be open at once

    # If alg dropdown pressed then metric dropdown
    if dropdown_alg == True and dropdown_metric == False:
        dropdown_alg, a_star, dijkstra = __alg_bar(window, dropdown_alg, a_star, dijkstra, width, height)
        dropdown_metric, distance, time = __metric_bar(window, dropdown_metric, distance, time, width, height) 
        if dropdown_metric == True:
            dropdown_alg = False
    
    # If metric dropdown pressed then alg dropdown
    elif dropdown_alg == False and dropdown_metric == True:
        dropdown_alg, a_star, dijkstra = __alg_bar(window, dropdown_alg, a_star, dijkstra, width, height)
        dropdown_metric, distance, time = __metric_bar(window, dropdown_metric, distance, time, width, height) 
        if dropdown_alg == True:
            dropdown_metric = False
    
    # If neither are dropdown
    else:
        dropdown_alg, a_star, dijkstra = __alg_bar(window, dropdown_alg, a_star, dijkstra, width, height)
        dropdown_metric, distance, time = __metric_bar(window, dropdown_metric, distance, time, width, height)        

    return dropdown_alg, a_star, dijkstra, dropdown_metric, distance, time