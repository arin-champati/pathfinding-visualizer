import pygame as pg
from config import Colors, Fonts
from functools import partial


def text_objects(text, font, color):
    """
    text: (string) desired text to be rendered
    font: (font) font object
    color: (int, int, int)

    summary: returns text surface and bounding rectangle
    """
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def create_button(window, button_event, default_action, pressed_action, font_size, text, active_color, inactive_color, x, y, w, h):
    """
    window: (pygame window)
    button_event: (pygame event) pygame event that is either MOUSEBUTTONDOWN or MOUSEBUTTON UP
    default_action: (lambda function) what the mouse returns if not pressed
    pressed_action: (lambda function) what the mouse returns if pressed
    font_size: (int) desired text font size
    text: (string) desired text to be displayed
    active_color: (int, int, int) color when hovered
    inactive_color: (int, int, int) default color
    rows: (int) number of rows
    x: (int) pixel x value of button
    y: (int) pixel y value of button
    w: (int) pixel width of button
    h: (int) pixel height of button

    summary: create a button with specified macros. When pressed, run a pressed action. Otherwise, return default action

    """
    mouse = pg.mouse.get_pos()

    result = partial(default_action)

    # check if the mouse location is within the button bounding box
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pg.draw.rect(window, active_color, (x, y, w, h))
        if button_event == pg.MOUSEBUTTONUP:
            result = partial(pressed_action)
    else:
        pg.draw.rect(window, inactive_color, (x, y, w, h))
    
    small_text = pg.font.Font(Fonts.BUTTON, int(font_size))
    text_surf, text_rect = text_objects(text, small_text, Colors.TEXT)
    text_rect.center = ((x + (w/2), y + (h / 2)))
    window.blit(text_surf, text_rect)

    return result()