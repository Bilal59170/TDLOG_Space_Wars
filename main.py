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

from UI import StartMenu, DeathMenu

def start_game():
    game = Game(profile=False)
    game_logic.activate_collision(game)
    game_logic.activate_asteroid_spawn(game)
    game_logic.activate_FPS_counter(game)
    game.run()

if __name__ == "__main__":
    # menu = StartMenu()
    # menu.start_game = start_game
    menu = StartMenu()
    pyglet.app.run()

