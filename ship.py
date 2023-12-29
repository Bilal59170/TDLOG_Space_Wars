""" Classe du vaisseau principal """
"""
Implémentation du vaisseau

Implémente Entity
"""
import config
import numpy as np
import pyglet
from pyglet.shapes import Polygon
import projectiles

import sprites, entity

class Ship(sprites.Polygon, pyglet.event.EventDispatcher):
    """ Classe du vaisseau principal """

    # Taille du vaisseau
    size = 10

    def __init__(self, pos, size, acceleration, max_speed, game_state):
        # Code de Bilal

        V1 = np.array([0, Ship.size])
        V2 = -Ship.size * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])
        V3 = Ship.size * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])

        vertices = np.array([V1, V2, V3]).astype(int)
        sprites.Polygon.__init__(self, pos, vertices, game_state, fillColor=(255,0,0))
        pyglet.event.EventDispatcher.__init__(self)

        self.acceleration = acceleration
        self.max_speed = max_speed

    def tick(self):
        """Fonction qui met à jour la position en fonction de la vitesse"""
        super().tick()

    def get_angle(self, x, y):
        """Fonction qui donne l'angle entre la position du vaisseau et celle d'un
        point (x,y)"""
        delta_x = x - self.screen_x
        delta_y = y - self.screen_y
        self.theta = np.arctan2(delta_y, delta_x)

    
    @property
    def border(self):
        is_border = {'UP': True, 'RIGHT': True,'DOWN': True,'LEFT': True}
        is_border['UP'] = (self.pos[1] - config.WIN_SIZE[1]/2) <= 0
        is_border['DOWN'] = (self.pos[1] + config.WIN_SIZE[1]/2) >= config.MAP_SIZE[1]
        is_border['LEFT'] = (self.pos[0] - config.WIN_SIZE[0]/2) <= 0
        is_border['RIGHT'] = (self.pos[0] + config.WIN_SIZE[0]/2) >= config.MAP_SIZE[0]

        return is_border
    
    
    def draw(self, batch=None):

        super().draw(batch)


    def on_mouse_motion(self, x, y, dx, dy):
        self.get_angle(x, y)

    def throw_projectile(self, speed):
        speed = 0
        p = projectiles.Projectile(self.x, self.y, speed*np.cos(self.theta), speed*np.sin(self.theta), 4, color = "r", game_state=self.game_state)
        return p
    
