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

from asteroids.asteroids import *

if __name__ == "__main__":  
    game = Game()

    pos = [0, 0]
    speed = [0, 0]
    vertices = create_nagon_vertices(5, 100)
    
    
    sprite = PolygonSprite(pos, speed, vertices, (255,255,0))
    sprite.game_state = game
    game.asteroids.append(sprite)
    game.entities.append(sprite)

    asteroid = BigAsteroid([100, 100], [0, 0], game)
    game.asteroids.append(asteroid)
    game.entities.append(asteroid)

    game.run()