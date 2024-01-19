import pyglet
from game_engine.utils import *
import pyglet.window.key as key

class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rectangle = pyglet.shapes.Rectangle(x - width/2, y - height/2, width, height, color=(255, 255, 255))
        self.text = pyglet.text.Label(text,
                                      font_name='Arial',
                                      font_size=18,
                                      color=(0, 0, 0, 255),
                                      x=x, y=y,
                                      anchor_x='center', anchor_y='center')
        
    def draw(self) :
        self.rectangle.draw()
        self.text.draw()
        




    def on_mouse_press(self, x, y, button, modifiers):
        if self.x - self.width // 2 < x < self.x + self.width // 2 and \
            self.y - self.height // 2 < y < self.y + self.height // 2:
            return True
        return False

# Exactement la même classe mais qui utilise la classe button
class StartMenu:
    def __init__(self):
        self.window = pyglet.window.Window(width=800, height=600, caption="Game Menu")
        self.batch = pyglet.graphics.Batch()
        self.labels = []

        self.window.on_draw = self.on_draw

        self.window.on_mouse_press = self.on_mouse_press

        self.window.on_text = self.on_text
        self.window.on_key_press = self.on_key_press
        
        Y_LABEL = 200

        self.labels.append(pyglet.text.Label('Pied.io: the new Diep.io',
                                             font_name='Arial',
                                             font_size=24,
                                             x=self.window.width // 2, y=Y_LABEL,
                                             anchor_x='center', anchor_y='center'))
        
        self.player_name = read_scoreboard()[-1][1]
        self.player_name_label = pyglet.text.Label('Player : ' + self.player_name,
                                                font_name='Arial',
                                                font_size=24,
                                                x=self.window.width // 4, y=self.window.height-100-200-50,
                                                anchor_x='left', anchor_y='center')

        self.play_button = Button(self.window.width // 4, Y_LABEL - 100, 100, 50, "Jouer")
        self.quit_button = Button(3*(self.window.width // 4), Y_LABEL - 100, 100, 50, "Quitter")
        self.make_grid()

    def on_draw(self):
        self.window.clear()
        self.labels[0].draw()
        self.play_button.draw()
        self.quit_button.draw()
        self.text.draw()
        self.player_name_label.draw()


    def on_mouse_press(self, x, y, button, modifiers):
        if self.play_button.on_mouse_press(x, y, button, modifiers):
            self.window.close()
            self.start_game(self.player_name)

        elif self.quit_button.on_mouse_press(x, y, button, modifiers):
            self.window.close()

    def make_grid(self):
        scores = read_scoreboard()
        lines = []
        for score, player in scores:
            lines += [f"{player:.<20} : {score}"]

        print('\n'.join(lines))
        
        document = pyglet.text.document.FormattedDocument('\n'.join(lines))
        document.set_style(0,len(document.text),dict(color=(255,255,255,255), font_size=21, font_name="Consolas"))
        self.text = pyglet.text.layout.ScrollableTextLayout(document,int(self.window.width / 1.7),200, multiline=True)
        self.text.x = self.window.width // 4
        self.text.y=self.window.height-100
        self.text.anchor_y="top"


    def on_text(self, text):
        self.player_name += text
        self.player_name_label.text = "Player : " + self.player_name

    def on_key_press(self, symbol, modifiers):
        for el in dir(key):
            if symbol == el:
                print(el.__name__)
        if symbol == key.DELETE or symbol == key.BACKSPACE:
            self.player_name = self.player_name[:-1]
            self.player_name_label.text = "Player : " + self.player_name



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
    )

    rectangle.opacity = 100
    rectangle.draw()

    game.mission_failed_sprite.draw()

    game.death_menu_batch.draw()

    #Affichage Boutons
    game.death_menu_buttons[0].rectangle.draw()
    game.death_menu_buttons[1].rectangle.draw()

    game.death_menu_buttons[0].text.draw()
    game.death_menu_buttons[1].text.draw()

    # On vérifie si le clic gauche est appuyé
    if game.mousebuttons[pyglet.window.mouse.LEFT]:

        if game.death_menu_buttons[0].on_mouse_press(game.mouse_x, game.mouse_y, 1, None):
            game.reset()
        
        elif game.death_menu_buttons[1].on_mouse_press(game.mouse_x, game.mouse_y, 1, None):
            game.window.close()
            import sys
            sys.exit()

from game_engine.utils import *
def death_menu_first_time(game):
    append_new_score(game.score, game.player_name)   
    # Affichage du game over et du score
    x_center = game.camera.size[0] // 2

    game.death_menu_batch = pyglet.graphics.Batch()

    mission_failed_img = pyglet.image.load("resources/Sprites/mission_failed.png")
    mission_failed_img.anchor_x = mission_failed_img.width // 2
    mission_failed_img.anchor_y = mission_failed_img.height // 2
    game.mission_failed_sprite = pyglet.sprite.Sprite(mission_failed_img, x=x_center, y=game.camera.size[1] // 2 + 170)

    pyglet.text.Label(
        f"Player : {game.player_name} \n Score : {game.score}",
        font_name='Arial',
        font_size=30,
        x=x_center, y=game.camera.size[1] // 2,
        anchor_x='center', anchor_y='center',
        color=(255,255,255,255),
        batch=game.death_menu_batch, multiline=True, width=300)
    
    
    # Bouton rejouer
    rejouer_button = Button(
        x_center, game.camera.size[1] // 2 - 100,
        100, 50,
        "Rejouer"
    )

    # Bouton quitter
    quitter_button = Button(
        x_center, game.camera.size[1] // 2 - 150,
        100, 50,
        "Quitter"
    )

    game.death_menu_batch.draw()
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
    if lvl == len(game.score_steps) :
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
        f"lvl : {lvl+1}  Xp : {game.score} / {game.score_steps[lvl]}" if lvl != len(game.score_steps) else f"lvl : {lvl+1}",
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