"""@package docstring
Fichier où l'on intègre la boucle de jeu

Fait appel à l'UI pour l'affichage
L'instance de jeu est nommée game_state

"""
import pyglet
from ship import *
from projectiles import *
from enemies import *
import config
import numpy as np
from pyglet.window import key
from pyglet.window import mouse
from time import time




class Game:

    """ """

    def __init__(self):
        self.bool = False
        self.player = Ship(
            np.array([config.MAP_SIZE[0] / 2, config.MAP_SIZE[1] / 2]),
            np.array([0., 0.]), 20, 4, 3,
            config.SHIP_SIZE,
        )
        self.asteroids = []
        self.enemies = [Enemy(np.array([config.MAP_SIZE[0] / 4, config.MAP_SIZE[1] / 4]),
                               np.array([0.,0.]),30., 2., 2., time(), 300., 200.)]
        self.entities = [self.player] + self.asteroids + self.enemies
        self.time = 0
        self.old_time = time()
        self.window = pyglet.window.Window()
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)
        self.mousebuttons = mouse.MouseStateHandler()
        self.window.push_handlers(self.mousebuttons)
        self.mouse_x = 0
        self.mouse_y = 0
        self.batch = pyglet.graphics.Batch()

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            self.mouse_x, self.mouse_y = x, y

        @self.window.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            if self.mousebuttons[mouse.RIGHT]:
                self.mouse_x, self.mouse_y = x, y

    def remove(self, object):
        pass

    def update_speed(self):
        #self.keys = key.KeyStateHandler()
        #self.window.push_handlers(self.keys)
        t = time() - self.old_time
        self.old_time = time()
        #norme = np.linalg.norm(self.player.speed) + 0.0001
        
        if (self.keys[key.Z] or self.keys[key.UP]) and (abs(self.player.speed[1]) < self.player.max_speed or self.player.speed[1] < 0):
            self.player.speed += t*self.player.acceleration*np.array([0., 1.])
        if (self.keys[key.Q] or self.keys[key.LEFT]) and (abs(self.player.speed[0]) < self.player.max_speed or self.player.speed[0] > 0):
            self.player.speed += t*self.player.acceleration*np.array([-1., 0.])
        if (self.keys[key.S] or self.keys[key.DOWN]) and (abs(self.player.speed[1]) < self.player.max_speed or self.player.speed[1] > 0):
            self.player.speed += t*self.player.acceleration*np.array([0., -1.])
        if (self.keys[key.D] or self.keys[key.RIGHT]) and (abs(self.player.speed[0]) < self.player.max_speed or self.player.speed[0] < 0):
            self.player.speed += t*self.player.acceleration*np.array([1., 0.])

        # if self.keys[key.Z] or self.keys[key.UP]:
        #     self.player.speed += np.array([0., 1.])
        # if self.keys[key.Q] or self.keys[key.LEFT]:
        #     self.player.speed += np.array([-1., 0.])
        # if self.keys[key.S] or self.keys[key.DOWN]:
        #     self.player.speed += np.array([0., -1.])
        # if self.keys[key.D] or self.keys[key.RIGHT]:
        #     self.player.speed += np.array([1., 0.])

        #norme = np.linalg.norm(self.player.speed) + 0.0001
        #self.player.speed /= norme

    def update_angle(self, x, y):
        self.player.get_angle(x, y)

    def display(self):
        self.window.clear()
        for e in self.entities:
            e.draw(self.batch)

    def endgame(self):
        if self.keys[key.O]:
            self.bool = True

    def new_projectile(self):
        if self.mousebuttons[mouse.RIGHT]:
                self.entities.append(self.player.throw_projectile(20))

    def update_projectiles(self):
        if len(self.entities) > 1:
            for e in self.entities[1:]:
                if(e.is_out(0, config.MAP_SIZE[0], 0, config.MAP_SIZE[1])):
                    self.entities.remove(e)

    def update_enemies(self, player) :
        for e in self.enemies :
            e.close_in_and_out(player)

    def update(self, *other):
        self.new_projectile()
        self.update_projectiles()
        self.update_speed()
        self.update_enemies(self.player)
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