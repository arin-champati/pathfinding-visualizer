import pygame as pg
from config import Colors, Fonts
from functools import partial


# get the parameters needed to write text (surface and rectangle)
def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

# create a button with specified macros. When pressed, run a pressed action. Otherwise, return default action
def create_button(window, mouse_event, default_action, pressed_action, font_size, text, active_color, inactive_color, x, y, w, h):
    mouse = pg.mouse.get_pos()

    result = partial(default_action)

    # check if the mouse location is within the button bounding box
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pg.draw.rect(window, active_color, (x, y, w, h))
        if mouse_event == pg.MOUSEBUTTONUP:
            result = partial(pressed_action)
    else:
        pg.draw.rect(window, inactive_color, (x, y, w, h))
    
    small_text = pg.font.Font(Fonts.BUTTON, int(font_size))
    text_surf, text_rect = text_objects(text, small_text, Colors.WHITE)
    text_rect.center = ((x + (w/2), y + (h / 2)))
    window.blit(text_surf, text_rect)

    return result()