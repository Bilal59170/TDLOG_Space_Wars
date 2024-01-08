import numpy as np

import sys
sys.path.append("../")

from game_engine import entity, config
from game_engine.sprites import Polygon
from game_objects.projectiles import Projectile

from time import time

class Enemy(Polygon):

    size = 20
    acceleration = 0.1
    max_speed = 2
    engage_radius = 200
    caution_radius = 400
    projectile_speed = 15
    reload_speed = 10

    fill_color = (255, 0, 0)
    edge_color = (0, 0, 0)

    #def __init__(self, pos, size, acceleration, max_speed, engage_radius, caution_radius, game_state, speed=np.array([0,0])):
    def __init__(self, pos, game_state, speed=np.array([0,0])):
        
        V1 = np.array([0, self.size])
        V2 = - self.size * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])
        V3 = self.size * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])
        vertices = np.array([V1, V2, V3]).astype(int)

        super().__init__(pos, vertices, game_state, fillColor=self.fill_color, edgeColor=self.edge_color, lineWidth=2, speed=speed)

        self.old_time = time()
        self.reload = 0


    """Fonction qui met à jour la position en fonction de la vitesse"""

    def aim_at(self, player):
        delta_x = player.x - self.x
        delta_y = player.y - self.y
        self.theta = np.arctan2(delta_y, delta_x)

    def throw_projectile(self):
        speed = self.projectile_speed
        p = Projectile(self.x, self.y, speed*np.cos(self.theta), speed*np.sin(self.theta), radius=4, color = "r", game_state=self.game_state)
        return p
    
    def close_in_and_out(self, player):
        
        self.aim_at(player)

        t = time() - self.old_time
        self.old_time = time()
        
        norme_t1 = np.linalg.norm(self.speed) 
        norme_in_t2 = np.linalg.norm(self.speed + t*self.acceleration*np.array([np.cos(float(self.theta)), np.sin(float(self.theta))]))
        norme_out_t2 = np.linalg.norm(self.speed - t*self.acceleration*np.array([np.cos(float(self.theta)), np.sin(float(self.theta))]))

        distance_player = np.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)

        if (norme_in_t2 <= self.max_speed or norme_in_t2 <= norme_t1) and distance_player > self.engage_radius :
            self.speed += t*self.acceleration*np.array([np.cos(float(self.theta)), np.sin(float(self.theta))])

        if (norme_out_t2 <= self.max_speed or norme_out_t2 <= norme_t1) and distance_player < self.caution_radius :
            self.speed -= t*self.acceleration*np.array([np.cos(float(self.theta)), np.sin(float(self.theta))])

    def tick(self):
        self.close_in_and_out(self.game_state.player)
        super().tick()

    def shoot(self, player):
        P = None
        r = np.linalg.norm(self.pos - player.pos)
        if r <= self.caution_radius and r >= self.engage_radius:
            if self.reload % self.reload_speed == 0:
                P = self.throw_projectile()
            self.reload += 1
        return P