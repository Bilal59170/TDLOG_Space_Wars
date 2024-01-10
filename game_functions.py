
import pyglet

import game_engine.sprites as sprites
from game_engine.utils import *

import pyglet.gui

from UI import Button

import math
from PIL import Image


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

def death_menu(game):

    # On grise l'écran pour faire un effet de game over avec un fondu
    rectangle = pyglet.shapes.Rectangle(
        0, 0,
        game.camera.size[0], game.camera.size[1],
        color=(0,0,0),
        batch=game.death_menu_batch
    )

    rectangle.opacity = 100
    rectangle.draw()

    game.death_menu_batch.draw()

    # On vérifie si le clic gauche est appuyé
    if game.mousebuttons[pyglet.window.mouse.LEFT]:

        if game.death_menu_buttons[0].on_mouse_press(game.mouse_x, game.mouse_y, 1, None):
            game.reset()
        
        elif game.death_menu_buttons[1].on_mouse_press(game.mouse_x, game.mouse_y, 1, None):
            game.window.close()
            import sys
            sys.exit()


def death_menu_first_time(game):
    # Affichage du game over et du score
    x_center = game.camera.size[0] // 2

    game.death_menu_batch = pyglet.graphics.Batch()

    mission_failed_img = pyglet.image.load("resources/Sprites/mission_failed.png")
    mission_failed_img.anchor_x = mission_failed_img.width // 2
    mission_failed_img.anchor_y = mission_failed_img.height // 2
    mission_failed_sprite = pyglet.sprite.Sprite(mission_failed_img, x=x_center, y=game.camera.size[1] // 2 + 100, batch=game.death_menu_batch)

    pyglet.text.Label(
        f"GAME OVER",
        font_name='Arial',
        font_size=50,
        x=x_center, y=game.camera.size[1] // 2,
        anchor_x='center', anchor_y='center',
        color=(255,0,0,255),
        batch=game.death_menu_batch)

    pyglet.text.Label(
        f"Score : {game.score}",
        font_name='Arial',
        font_size=30,
        x=x_center, y=game.camera.size[1] // 2 - 50,
        anchor_x='center', anchor_y='center',
        color=(255,255,255,255),
        batch=game.death_menu_batch)
    
    
    # Bouton rejouer
    rejouer_button = Button(
        x_center, game.camera.size[1] // 2 - 100,
        100, 50,
        "Rejouer",
        game.death_menu_batch
    )

    # Bouton quitter
    quitter_button = Button(
        x_center, game.camera.size[1] // 2 - 150,
        100, 50,
        "Quitter",
        game.death_menu_batch
    )

    game.death_menu_buttons = [rejouer_button, quitter_button]



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
    if lvl == len(game.score_steps) - 1:
        prct = 1
    else:
        prct = game.score / game.score_steps[lvl]

    resources_prct = min(game.score / game.score_steps[-1] * 1.5, 1)

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

    if game.player_dead != "Alive":
        if not hasattr(game, "death_menu_batch") or game.death_menu_batch is None:
            death_menu_first_time(game)
        death_menu(game)