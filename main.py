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


if __name__ == "__main__":
    game = Game()

    sprite = nagonSprite(8, 10, (255, 0, 0))
    game.asteroids.append(sprite)
    game.entities.append(sprite)

    game.run()