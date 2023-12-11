"""
Implémentation du vaisseau
Implémentera Entity

"""
import numpy as np
import entity
from pyglet.shapes import Polygon

from collections.abc import Iterable
import pyglet

class Ship(entity.PolygonSprite, pyglet.event.EventDispatcher):

    size = 10

    def __init__(self, pos, speed, size, game_state=None):

        V1 = np.array([0, Ship.size])
        V2 = -Ship.size * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])
        V3 = Ship.size * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])

        vertices = np.array([V1, V2, V3]).astype(int)
        
        entity.PolygonSprite.__init__(self, pos, speed, vertices, game_state=game_state, fillColor=(255,0,0))
        pyglet.event.EventDispatcher.__init__(self)
        self.angle = 0
        self.size = size

    def tick(self):
        """Fonction qui met à jour la position en fonction de la vitesse"""
        entity.Entity.tick(self)

    def get_angle(self, x, y):
        """Fonction qui donne l'angle entre la position du vaisseau et celle d'un
        point (x,y)"""
        delta_x = x - self.screen_x
        delta_y = y - self.screen_y
        self.theta = np.arctan2(delta_y, delta_x)


    def draw(self, batch=None):
        """Fonction qui dessine un triangle equilatéral et l'oriente en fonction
        de l'angle. le parametre size est la distance entre le centre et un des
        3 points. """
        # On prend les coordonnées des sommets quand le triangle pointe vers
        # le haut puis on les tourne de -(pi/2 - theta) l'angle fait
        # avec la souris

        super().draw(batch)


    def on_mouse_motion(self, x, y, dx, dy):
        self.get_angle(x, y)
