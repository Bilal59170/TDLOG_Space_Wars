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

    def remove(self, object):
        pass

    def update_speed(self):
        keys = key.KeyStateHandler()
        self.window.push_handlers(keys)
        if keys[key.Z] or keys[key.UP]:
            self.player.speed = np.array([0, -1])
        elif keys[key.Q] or keys[key.LEFT]:
            self.player.speed = np.array([-1, 0])
        elif keys[key.S] or keys[key.DOWN]:
            self.player.speed = np.array([0, 1])
        elif keys[key.D] or keys[key.RIGHT]:
            self.player.speed = np.array([1, 0])

    def update_angle(self,x,y):
        self.player.get_angle(x,y)

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

    def run(self):
        self.display()
        while(self.endgame == False):
            self.update()
            keys = key.KeyStateHandler()
            self.window.push_handlers(keys)
            if keys[key.O]:
                self.endgame = True
        