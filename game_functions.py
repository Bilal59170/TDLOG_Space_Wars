
import pyglet

import game_engine.sprites as sprites
from game_engine.utils import *

import pyglet.gui

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

    if game.player.state != "Alive":
        # Affichage du game over et du score

        # On grise l'écran pour faire un effet de game over avec un fondu
        rectangle = pyglet.shapes.Rectangle(
            0, 0,
            game.camera.size[0], game.camera.size[1],
            color=(0,0,0),
        )
        rectangle.opacity = 100
        rectangle.draw()

        pyglet.text.Label(
            f"GAME OVER",
            font_name='Arial',
            font_size=50,
            x=x_center, y=game.camera.size[1] // 2,
            anchor_x='center', anchor_y='center',
            color=(255,0,0,255)).draw()

        pyglet.text.Label(
            f"Score : {game.score}",
            font_name='Arial',
            font_size=30,
            x=x_center, y=game.camera.size[1] // 2 - 50,
            anchor_x='center', anchor_y='center',
            color=(255,255,255,255)).draw()
        

        # Création de l'image de quand lebouton est appuyé
        img = Image.open("resources/Sprites/Buttons/Menu.png")
        img = img.resize((int(img.size[0] * 1.5), int(img.size[1] * 1.5)))
        img.save("resources/Sprites/Buttons/Menu_pressed.png")


        # Label rejouer
        label = pyglet.text.Label(
            f"Rejouer",
            font_name='Arial',
            font_size=30,
            x=x_center, y=game.camera.size[1] // 2 - 100,
            anchor_x='center', anchor_y='center',
            color=(255,255,255,255)).draw()
        # Bouton rejouer !
        pyglet.gui.PushButton(
            x=game.camera.size[0]//3,
            y=game.camera.size[1]//2 - 100,

            #on_press=game.restart,
            batch=game.batch
        )
