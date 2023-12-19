
import numpy as np
import pyglet

import sprites, entity

class Ship(sprites.Polygon, pyglet.event.EventDispatcher):

    size = 10

    def __init__(self, pos, size, game_state):

        V1 = np.array([0, Ship.size])
        V2 = -Ship.size * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])
        V3 = Ship.size * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])

        vertices = np.array([V1, V2, V3]).astype(int)
        sprites.Polygon.__init__(self, pos, vertices, game_state, fillColor=(255,0,0))
        pyglet.event.EventDispatcher.__init__(self)
        self.angle = 0
        self.size = size

    def tick(self):
        """Fonction qui met à jour la position en fonction de la vitesse"""
        super().tick()

    def get_angle(self, x, y):
        """Fonction qui donne l'angle entre la position du vaisseau et celle d'un
        point (x,y)"""
        delta_x = x - self.screen_x
        delta_y = y - self.screen_y
        self.theta = np.arctan2(delta_y, delta_x)


    def draw(self, batch=None):

        super().draw(batch)


    def on_mouse_motion(self, x, y, dx, dy):
        self.get_angle(x, y)
