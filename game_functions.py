
import pyglet

import game_engine.sprites as sprites
from game_engine.utils import *

import math


def draw_filled_bar(pos,
                width,
                height,
                spacing,
                filled_percent,
                primary_color,
                secondary_color,
                batch
                ):
        
    draw_bar(
        center = (pos[0], pos[1]-height),
        width = width,
        height = height,
        color = secondary_color,
        batch=batch
    )

    width = int(width - spacing * 2)
    
    draw_bar(
        center = (pos[0]- width * (1 - filled_percent)/2, pos[1]-height),
        width = width * filled_percent,
        height = height - spacing,
        color = primary_color,
        batch=batch
    )




def game_static_display(game):

    lvl_primary_color = (234,217,105)
    resources_primary_color = (102,240,160)

    lvl_secondary_color = (55,61,58)
    resources_secondary_color = (55,61,58)

    x_center = game.camera.size[0] // 2
    y_center_lvl = 35
    y_center_resources = 60

    spacing = 5

    lvl_width = game.camera.size[0] // 6
    lvl_height = 20

    resources_width = game.camera.size[0] // 10
    resources_height = 20

    draw_filled_bar(
        (x_center, y_center_lvl),
        lvl_width,
        lvl_height,
        spacing,
        1,
        lvl_primary_color,
        lvl_secondary_color,
        game.batch
    )

    draw_filled_bar(
        (x_center, y_center_resources),
        resources_width,
        resources_height,
        spacing,
        1,
        resources_primary_color,
        resources_secondary_color,
        game.batch
    )

    game.hurt_animation()

