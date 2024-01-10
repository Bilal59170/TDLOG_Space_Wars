import numpy as np
from time import time

import pyglet
from pyglet.window import key, mouse

pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

from game_engine.config import *
from game_engine import sprites
from game_objects.ship import Ship
from game_objects.asteroids import *
from game_objects.enemies import *
from game_objects.projectiles import *
from game_objects.animations import XPLosion

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

    # Création de la partie
    game = Game(profile=False)

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


    img_caca = pyglet.image.load("resources/Sprites/caca.png")

    if(False):
            # Deux cacas. Le deuxième va plus vite et est incliné (normalement) (ne fonctionne pas !)
        caca = sprites.Image(np.array([-500, 0]), img_caca, game)
        caca2 = sprites.Image(np.array([500, 0]), img_caca, game, speed=[-10, 0], theta=np.pi/6)

        game.add_entity(caca)
        game.add_entity(caca2)

        # Ajout d'une image animées ! Les images sont dans le dossier Sprites/animation, et sont nommées an_1.png, an_2.png, etc.
        # Elles sont ensuite chargées dans une liste, puis transformées en animation.
        images = [pyglet.image.load(f'resources/Sprites/animation/an_{i}.png') for i in range(1, 6)]
        animation = pyglet.image.Animation.from_image_sequence(images, .5)

        # L'image animée est ensuite ajoutée au jeu, comme pour une image normale.
        img = sprites.Image(np.array([0, 0]), animation, game)
        game.add_entity(img)

    # Logique de jeu => Collision et spawn d'astéroïdes
    game_logic.activate_collision(game)
    game_logic.activate_asteroid_spawn(game)
    game_logic.activate_FPS_counter(game)

    game.run()
