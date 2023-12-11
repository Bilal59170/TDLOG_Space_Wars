"""
Implémentation du vaisseau
Implémentera Entity

"""
import numpy as np
import entity
from pyglet.shapes import Polygon

from collections.abc import Iterable
import pyglet

class Ship(entity.Entity, pyglet.event.EventDispatcher):
    def __init__(self, pos, speed, size, game_state=None):
        entity.Entity.__init__(self, pos, speed, game_state=game_state)
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
        self.angle = np.arctan2(delta_y, delta_x)
    
    @property
    def rotation_matrix(self):
        theta = self.angle
        rot = np.array([
                [np.cos(np.pi / 2 - theta), np.sin(np.pi / 2 - theta)],
                [-np.sin(np.pi / 2 - theta), np.cos(np.pi / 2 - theta)],
            ])
        return rot
    


    def draw(self, batch=None):
        """Fonction qui dessine un triangle equilatéral et l'oriente en fonction
        de l'angle. le parametre size est la distance entre le centre et un des
        3 points. """
        # On prend les coordonnées des sommets quand le triangle pointe vers
        # le haut puis on les tourne de -(pi/2 - theta) l'angle fait
        # avec la souris

        rot = self.rotation_matrix

        V1 = self.screen_pos + np.dot(rot, np.array([0, self.size]))
        V2 = self.screen_pos + np.dot(
            rot, -self.size * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])
        )
        V3 = self.screen_pos + np.dot(
            rot, self.size * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])
        )

        vertices = np.array([V1, V2, V3]).astype(int)
        
        if batch is None:
            Polygon(*vertices, color=(255, 0, 0)).draw()
        else:
            triangle = pyglet.shapes.Polygon(*vertices, color=(255, 0, 0), batch=batch)
            triangle.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.get_angle(x, y)
