"""@package docstring
Fichier où l'on intègre la boucle de jeu

Fait appel à l'UI pour l'affichage
L'instance de jeu est nommée game_state

"""
import pyglet
from ship import *
from projectiles import *
import config
import numpy as np
from pyglet.window import key
from pyglet.window import mouse


class Game:

    """ """

    def __init__(self):
        self.bool = False
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
        self.mousebuttons = mouse.MouseStateHandler()
        self.window.push_handlers(self.mousebuttons)
        self.mouse_x = 0
        self.mouse_y = 0

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            self.mouse_x, self.mouse_y = x, y


    def remove(self, object):
        pass

    def update_speed(self):
        if self.keys[key.Z] or self.keys[key.UP]:
            self.player.speed = np.array([0, 1])
        elif self.keys[key.Q] or self.keys[key.LEFT]:
            self.player.speed = np.array([-1, 0])
        elif self.keys[key.S] or self.keys[key.DOWN]:
            self.player.speed = np.array([0, -1])
        elif self.keys[key.D] or self.keys[key.RIGHT]:
            self.player.speed = np.array([1, 0])

    def update_angle(self, x, y):
        self.player.get_angle(x, y)

    def display(self):
        self.window.clear()
        for e in self.entities:
            e.draw()

    def endgame(self):
        if self.keys[key.O]:
            self.bool = True

    def new_projectile(self):
        print("a")
        print(self.mousebuttons[mouse.RIGHT])
        if self.mousebuttons[mouse.RIGHT]:
                self.entities.append(self.player.throw_projectile())
                print("monstre")

    def update(self, *other):
        self.update_speed()
        self.time += config.TICK_TIME
        for e in self.entities:
            e.tick()
        self.update_angle(self.mouse_x, self.mouse_y)
        if self.time % config.FRAME_TIME:
            self.display()

    # fonction boucle principale
    def run(self):
        self.display()
        while self.bool is False:
            self.update()
            self.new_projectile()
            print("monstre")