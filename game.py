"""
Fichier où l'on intègre la boucle de jeu
Fait appel à l'UI pour l'affichage
L'instance de jeu est nommée game_state

"""
import pyglet
import ship
import config
import numpy as np

class Game:

    """ """

    def __init__(self):
        self.endgame = False
        self.player = ship(
            np.arrey([config.MAP_SIZE[0] / 2, config.MAP_SIZE[1] / 2]),
            np.array([0, 0]),
            config.SIZE_SHIP,
        )
        self.asteroids = []
        self.ennemies = []
        self.time = 0
        self.window = pyglet.window.Window()

    def remove(self, object):
        pass

    def display(self):
        self.window.clear()
        self.player.draw()
        for a in self.asteroids:
            a.draw()
        for e in self.ennemies:
            e.draw()

    def update(self):
        self.time += config.TICK_TIME
        self.player.tick()
        for a in self.asteroids:
            a.tick()
        for e in self.ennemies:
            e.tick()
        if self.time % config.FRAME_TIME:
            self.display()


