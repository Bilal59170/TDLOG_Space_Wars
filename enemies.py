import numpy as np
import entity
from pyglet.shapes import Polygon
import projectiles
from time import time

class Enemy(entity.Entity):
    def __init__(self, pos, speed, size, acceleration, max_speed, old_time, engage_radius, caution_radius, game_state=None):
        super().__init__(pos, speed, game_state)
        self.angle = 0
        self.size = size
        self.acceleration = acceleration
        self.max_speed = max_speed
        self.old_time = old_time
        self.engage_radius = engage_radius
        self.caution_radius = caution_radius

    """Fonction qui met à jour la position en fonction de la vitesse"""

    def update_pos(self):
        self.tick(self)

    def aim_at(self, player):
        delta_x = player.x - self.x
        delta_y = player.y - self.y
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
    
    def is_out(self, x_min, x_max, y_min, y_max):
        return False
    
    def close_in_and_out(self, player):
        
        self.aim_at(player)

        t = time() - self.old_time
        self.old_time = time()
        
        norme_t1 = np.linalg.norm(self.speed) 
        norme_in_t2 = np.linalg.norm(self.speed + t*self.acceleration*np.array([np.cos(float(self.angle)), np.sin(float(self.angle))]))
        norme_out_t2 = np.linalg.norm(self.speed - t*self.acceleration*np.array([np.cos(float(self.angle)), np.sin(float(self.angle))]))

        distance_player = np.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)

        if (norme_in_t2 <= self.max_speed or norme_in_t2 <= norme_t1) and distance_player > self.engage_radius :
            self.speed += t*self.acceleration*np.array([np.cos(float(self.angle)), np.sin(float(self.angle))])

        if (norme_out_t2 <= self.max_speed or norme_out_t2 <= norme_t1) and distance_player < self.caution_radius :
            self.speed -= t*self.acceleration*np.array([np.cos(float(self.angle)), np.sin(float(self.angle))])