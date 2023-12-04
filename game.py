"""@package docstring
Fichier où l'on intègre la boucle de jeu

Fait appel à l'UI pour l'affichage
L'instance de jeu est nommée game_state

"""
import pyglet
from ship import *
import config
import numpy as np
from pyglet.window import key


class Game:

    """ """

    def __init__(self):
        self.endgame = False
        self.player = Ship(
            np.array([config.MAP_SIZE[0] / 2, config.MAP_SIZE[1] / 2]),
            np.array([0, 0]),
            config.SHIP_SIZE,
        )
        self.asteroids = []
        self.ennemies = []
        self.entities = [self.player] + self.asteroids + self.ennemies
        self.time = 0
        self.window = pyglet.window.Window()
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)

    def remove(self, object):
        pass

    def update_speed(self):
        #self.keys = key.KeyStateHandler()
        #self.window.push_handlers(self.keys)
        if self.keys[key.Z] or self.keys[key.UP]:
            self.player.speed = np.array([0, -1])
        elif self.keys[key.Q] or self.keys[key.LEFT]:
            self.player.speed = np.array([-1, 0])
        elif self.keys[key.S] or self.keys[key.DOWN]:
            self.player.speed = np.array([0, 1])
        elif self.keys[key.D] or self.keys[key.RIGHT]:
            self.player.speed = np.array([1, 0])

    def update_angle(self, x, y):
        self.player.get_angle(x, y)

    def display(self):
        self.window.clear()
        for e in self.entities:
            e.draw()

    def update(self):
        self.update_speed()
        self.time += config.TICK_TIME
        for e in self.entities:
            e.tick()
        x, y = pyglet.window.mouse.get_pos()
        self.update_angle(x, y)
        if self.time % config.FRAME_TIME:
            self.display()

    # fonction boucle principale
    def run(self):
        self.display()
        while self.endgame is False:
            self.update()
            keys = key.KeyStateHandler()
            self.window.push_handlers(keys)
            if keys[key.O]:
                self.endgame = True
