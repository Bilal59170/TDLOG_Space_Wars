"""@package docstring
Implémentation du vaisseau

Implémente Entity
"""
import numpy as np
import entity
from pyglet.shapes import Polygon
import projectiles


class Ship(entity.Entity):
    def __init__(self, pos, speed, size, game_state=None):
        super().__init__(pos, speed, game_state)
        self.angle = 0
        self.size = size

    """Fonction qui met à jour la position en fonction de la vitesse"""

    def update_pos(self):
        self.tick(self)

    """Fonction qui donne l'angle entre la position du vaisseau et celle d'un
      point (x,y)"""

    def get_angle(self, x, y):
        delta_x = x - self.pos[0]
        delta_y = y - self.pos[1]
        self.angle = np.arctan2(delta_y, delta_x)

    """Fonction qui dessine un triangle equilatéral et l'oriente en fonction
    de l'angle. le parametre size est la distance entre le centre et un des
    3 points. """

    def draw(self, batch):
        # On prend les coordonnées des sommets quand le triangle pointe vers
        # le haut puis on les tourne de -(pi/2 - theta) l'angle fait
        # avec la souris

        theta = self.angle
        rot = np.array(
            [
                [np.cos(np.pi / 2 - theta), np.sin(np.pi / 2 - theta)],
                [-np.sin(np.pi / 2 - theta), np.cos(np.pi / 2 - theta)],
            ]
        )
        V1 = self.pos + np.dot(rot, np.array([0, self.size]))
        V2 = self.pos + np.dot(
            rot, -self.size * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])
        )
        V3 = self.pos + np.dot(
            rot, self.size * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])
        )

        vertices = np.array([V1, V2, V3]).astype(int)
        triangle = Polygon(*vertices, color=(0, 255, 0), batch=batch) #opérateur *: unpack
        triangle.draw()

    def throw_projectile(self, speed):
        p = projectiles.Projectile(self.x, self.y, speed*np.cos(self.angle), speed*np.sin(self.angle), 4, color = "r")
        return p
    