# gestion du jeu
from game import Game
import game_logic

from pyglet.gl import *
# pyglet.gl.glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)                             
# pyglet.gl.glEnable (GL_BLEND)                                                            
# pyglet.gl.glEnable (GL_LINE_SMOOTH);                                                     
# pyglet.gl.glHint (GL_LINE_SMOOTH_HINT, GL_DONT_CARE)                                     


"""@package docstring
Fichier d'application (sert pour l'instant à tester le code produit)


"""

"""
    Fichier principal du jeu.
    Initie le jeu, ses différentes entités et lance la boucle principale.
"""

# import des astéroïdes

if __name__ == "__main__":


    # Ajout de quatre astéroïdes de tailles différentes sur les quatre coins de la carte
    spacing = 50

    if(False):
        asteroid = MasterAsteroid([spacing, 0], game) # Un gros astéroïde !
        game.add_entity(asteroid)

        asteroid = BigAsteroid([MAP_SIZE[0]-spacing, 0], game)
        game.add_entity(asteroid)

        asteroid = SmallAsteroid([0, MAP_SIZE[1]-spacing], game)
        game.add_entity(asteroid)

        asteroid = MediumAsteroid([MAP_SIZE[0]-spacing, MAP_SIZE[1]-spacing], game)
        game.add_entity(asteroid)

    # Ajout de textes indiquant les coordonnées à différents endroits de la carte, sur une grille de 5x5
    # n = 5
    # for x in range(0, MAP_SIZE[0], MAP_SIZE[0] // n):
    #     for y in range(0, MAP_SIZE[1], MAP_SIZE[1] // n):
    #         text = sprites.Label([x, y], f"{x}, {y}", game, color=(0,0,0,255))
    #         game.add_entity(text)





import pyglet
from pyglet.window import key
import game_logic
from game import Game

class Menu:
    def __init__(self):
        self.window = pyglet.window.Window(width=800, height=600, caption="Game Menu")
        self.batch = pyglet.graphics.Batch()
        self.labels = []

        self.labels.append(pyglet.text.Label('New Diep.io',
                                             font_name='Arial',
                                             font_size=24,
                                             x=self.window.width // 2, y=self.window.height // 2,
                                             anchor_x='center', anchor_y='center', batch=self.batch))

        self.play_button = pyglet.text.Label('Jouer',
                                             font_name='Arial',
                                             font_size=18,
                                             x=self.window.width // 4, y=self.window.height // 2 - 100,
                                             anchor_x='center', anchor_y='center', batch=self.batch)
        
        self.quit_button = pyglet.text.Label('Quitter',
                                             font_name='Arial',
                                             font_size=18,
                                             x=3*(self.window.width // 4), y=self.window.height // 2 - 100,
                                             anchor_x='center', anchor_y='center', batch=self.batch)

    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.play_button.x - self.play_button.content_width // 2 < x < self.play_button.x + self.play_button.content_width // 2 and \
            self.play_button.y - self.play_button.content_height // 2 < y < self.play_button.y + self.play_button.content_height // 2:
            self.window.close()
            start_game()
        elif self.quit_button.x - self.quit_button.content_width // 2 < x < self.quit_button.x + self.quit_button.content_width // 2 and \
            self.quit_button.y - self.quit_button.content_height // 2 < y < self.quit_button.y + self.quit_button.content_height // 2:
            self.window.close()

def start_game():
    game = Game(profile=False)
    game_logic.activate_collision(game)
    game_logic.activate_asteroid_spawn(game)
    game_logic.activate_FPS_counter(game)
    game.run()

if __name__ == "__main__":
    menu = Menu()

    @menu.window.event
    def on_draw():
        menu.on_draw()

    @menu.window.event
    def on_mouse_press(x, y, button, modifiers):
        menu.on_mouse_press(x, y, button, modifiers)

    pyglet.app.run()

