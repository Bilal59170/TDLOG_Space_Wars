"""
Fichier où l'on intègre la boucle de jeu
Fait appel à l'UI pour l'affichage
L'instance de jeu est nommée game_state

"""

import ship
import config


class Game:

    """ """

    def __init__(self):
        self.endgame = False
        self.player = ship(
            [config.MAP_SIZE[0] / 2, config.MAP_SIZE[1] / 2],
            config.SPEED_FACTOR,
            config.SIZE_SHIP,
        )
        self.asteroids = []
        self.ennemies = []
        self.time = 0

    def remove(self, object):
        pass

    def update(self):
        self.time += config.TICK_TIME
