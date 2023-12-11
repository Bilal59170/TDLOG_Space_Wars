"""
    Scénario d'une partie :
    Génération initiale de terrain (skip for v1)
    Création du personnage joueur
    Affichage de la fenêtre
    game_time = 0

    Boucle principale de jeu (tant que l'utilisateur ne met pas fin au jeu, ou que vaisseau.PV > 0):
    game_time += TICK_TIMESTEP
    récupérer les événements : position de souris, clic
    game.tick() (for all entities in game: entity.tick())
    si game_time % FRAME_TIME == 0:
        affichage
"""
import pyglet
from pyglet.window import key, mouse
from game import Game
from entity import *
import config

from asteroids.asteroids import *

if __name__ == "__main__":  
    game = Game()

    pos = [0, 0]
    speed = [0, 0]
    vertices = create_nagon_vertices(5, 100)
    print(vertices.shape)
    
    
    sprite = PolygonSprite(pos, speed, vertices, fillColor=(255,255,0))
    sprite.game_state = game
    game.asteroids.append(sprite)
    game.entities.append(sprite)

    asteroid = BigAsteroid([100, 100], [0, 0], game)
    game.asteroids.append(asteroid)
    game.entities.append(asteroid)

    game.run()


""" LES TESTS DE BIL """


# img_caca = pyglet.image.load("Sprites/caca.png")
# sprite_caca = pyglet.sprite.Sprite(img_caca, x=0, y=0)

# # if __name__ == "__main__":
# game_window = pyglet.window.Window()

# @game_window.event
# def on_draw():
#     # game_window.clear()
#     sprite_caca.draw()

# pyglet.app.run()
    


    # game = Game()

    # sprite = nagonSprite(8, 10, (255, 0, 0))
    # game.asteroids.append(sprite)
    # game.entities.append(sprite)

        # caca = BitmapSprite(np.array([config.MAP_SIZE[0] / 2, config.MAP_SIZE[1] / 2]),
    #         np.array([0, 0]), img_caca)
    #game.run()
