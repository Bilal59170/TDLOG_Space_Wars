"""
Implémentation du vaisseau
Implémentera Entity

"""
import numpy as np
import entity
from pyglet.shapes import Polygon


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
        return np.arctan2(delta_y, delta_x)

    """Fonction qui dessine un triangle equilatéral et l'oriente en fonction
    de l'angle. le parametre size est la distance entre le centre et un des
    3 points. """

    def draw(self, x, y):
        # On prend les coordonnées des sommets quand le triangle pointe vers
        # le haut puis on les tourne de -(pi/2 - theta) l'angle fait
        # avec la souris

        theta = self.get_angle(self, x, y)
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

        vertices = [V1[0], V1[1], V2[0], V2[1], V3[0], V3[1]]
        triangle = Polygon(vertices, color=(255, 0, 0))
        triangle.draw()
