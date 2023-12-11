import numpy as np
import entity
from pyglet.shapes import Polygon
import projectiles

class Enemies(entity.Entity):
    def __init__(self, pos, speed, size, game_state=None):
        super().__init__(pos, speed, game_state)
        self.angle = 0
        self.size = size

    """Fonction qui met à jour la position en fonction de la vitesse"""

    def update_pos(self):
        self.tick(self)

    def aim_at(self, player):
        delta_x = player.x - self.pos[0]
        delta_y = player.y - self.pos[1]
        self.angle = np.arctan2(delta_y, delta_x)

    def throw_projectile(self, speed):
        p = projectiles.Projectile(self.x, self.y, speed*np.cos(self.angle), speed*np.sin(self.angle), 4, color = "r")
        return p
    
    def draw(self, batch):
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
        triangle = Polygon(*vertices, color=(255, 0, 0), batch=batch) #opérateur *: unpack
        triangle.draw()

    def throw_projectile(self, speed):
        p = projectiles.Projectile(self.x, self.y, speed*np.cos(self.angle), speed*np.sin(self.angle), 4, color = "r")
        return p