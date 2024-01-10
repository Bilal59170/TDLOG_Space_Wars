
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
        center = (pos[0], pos[1]),
        width = width,
        height = height,
        color = secondary_color,
        batch=batch
    )

    new_width = int(height / 2 + (width - spacing * 2 - height / 2) * filled_percent)

    height = int(height - spacing * 2)

    new_x_center = pos[0] - width / 2 + spacing + new_width / 2

    draw_bar(
        center = (new_x_center, pos[1]),
        width = new_width,
        height = height,
        color = primary_color,
        batch=batch
    )




def game_static_display(game):

    lvl_primary_color = (234,217,105)
    resources_primary_color = (102,240,160)

    lvl_secondary_color = (55,61,58)
    resources_secondary_color = (55,61,58)

    x_center = game.camera.size[0] // 2
    y_center_lvl = 30
    y_center_resources = 70

    spacing = 5

    lvl_width = game.camera.size[0] // 3.2
    lvl_height = 30

    resources_width = game.camera.size[0] // 4
    resources_height = 30

    lvl = game.player.level
    print(f"lvl {lvl} len {len(game.score_steps)}")
    if lvl == len(game.score_steps) - 1:
        prct = 1
    else:
        prct = game.score / game.score_steps[lvl]

    resources_prct = game.score / game.score_steps[-1] * 1.5

    draw_filled_bar(
        (x_center, y_center_lvl),
        lvl_width,
        lvl_height,
        spacing,
        prct,
        lvl_primary_color,
        lvl_secondary_color,
        game.batch
    )

    draw_filled_bar(
        (x_center, y_center_resources),
        resources_width,
        resources_height,
        spacing,
        resources_prct,
        resources_primary_color,
        resources_secondary_color,
        game.batch
    )

    pyglet.text.Label(
        f"lvl : {lvl+1}  Xp : {game.score} / {game.score_steps[lvl]}",
        font_name='Calibri',
        font_size=11,
        x=x_center, y=y_center_lvl,
        anchor_x='center', anchor_y='center',
        color=(255,255,255,255)).draw()

    pyglet.text.Label(
        f"Resources : {game.score}",
        font_name='Arial',
        font_size=11,
        x=x_center, y=y_center_resources,
        anchor_x='center', anchor_y='center',
        color=(255,255,255,255)).draw()

    game.hurt_animation()

