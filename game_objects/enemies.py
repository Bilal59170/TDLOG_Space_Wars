import numpy as np

import sys
sys.path.append("../")

from game_engine import entity, config
from game_engine.sprites import Polygon
from game_objects.projectiles import Projectile
from game_engine.utils import draw_bar
from UI import draw_filled_bar

from time import time

class Enemy(Polygon):
    """
    size = 20
    acceleration = 0.1
    max_speed = 2
    engage_radius = 200
    caution_radius = 400
    projectile_speed = 15
    reload_speed = 10

    fill_color = (255, 0, 0)
    """
    edge_color = (0, 0, 0)   # Couleur du bord
    lineWidth = 5               # Taille de bord

    bar_grey = (128, 128, 128)  # Gris de la barre de vie
    bar_color = (0,128,0)       # Couleur de la barre de vie
    barWidthFactor = .8         # Longueur de la barre de vie (en % de la taille de l'ennemi)
    barHeight = 16              # Largeur de la barre de vie
    barSpacing = 2              # Largeur de la bordure
    """
    ressources = 100             # XP donnée en tuant l'ennemi
    max_HP = 100
    """
    max_HP_levels = [200, 500, 2000, 4000]
    ressources_levels = [100, 200, 500, 1000]
    size_levels = [20, 30, 40, 50]
    projectile_speed_levels = [15, 20, 25, 40]
    reload_speed_levels = [15, 10, 10, 8]
    damage_levels = [5, 10, 25, 100]
    acceleration_levels = [0.5, 0.7, 0.7, 1]
    max_speed_levels = [1, 2, 2, 3]
    engage_radius_levels = [100, 100, 75, 50]
    caution_radius_levels = [400, 500, 500, 450]
    fill_color_levels = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]

    #def __init__(self, pos, size, acceleration, max_speed, engage_radius, caution_radius, game_state, speed=np.array([0,0])):
    def __init__(self, pos, game_state, speed=np.array([0,0]), level=0):
        self.reload = self.reload_speed_levels[level]
        self.level = level
        self.max_HP = self.max_HP_levels[level]
        self._HP = self.max_HP
        self.max_speed = self.max_speed_levels[level]
        self.size = self.size_levels[level]
        self.projectile_speed = self.projectile_speed_levels[level]
        self.reload_speed = self.reload_speed_levels[level]
        self.ressources = self.ressources_levels[level]
        self.acceleration = self.acceleration_levels[level]
        self.engage_radius = self.engage_radius_levels[level]
        self.caution_radius = self.caution_radius_levels[level]
        self.fill_color = self.fill_color_levels[level]

        V1 = np.array([0, self.size])
        V2 = - self.size * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])
        V3 = self.size * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])
        vertices = np.array([V1, V2, V3]).astype(int)

        super().__init__(pos, vertices, game_state, fillColor=self.fill_color, edgeColor=self.edge_color, lineWidth=2, speed=speed)

        self.old_time = time()
        self.alive = True
        self._theta = 0

    @property
    def HP(self):
        return self._HP

    @property
    def rotation_matrix(self):
        M = np.array([[np.cos(self._theta), np.sin(self._theta)],
                     [-np.sin(self._theta), np.cos(self._theta)]])
        return M

    @HP.setter
    def HP(self, HP):
        if HP <= 0:
            self.die()
        self._HP = min(self.max_HP, HP)

    def die(self):
        """
        Fonction de mort de l'astéroïde
        """
        try:
            self.alive = False
            self.game_state.remove_entity(self)
            self.game_state.add_score(self.ressources)
        except ValueError:
            pass

    def draw(self, batch=None):
        """Dessine l'astéroïde"""
        super().draw(batch=batch)
        
        draw_filled_bar(
            (self.screen_pos[0], self.screen_pos[1]-self.size-self.barHeight),
            self.size*2*self.barWidthFactor,
            self.barHeight,
            self.barSpacing,
            self._HP/self.max_HP,
            self.fill_color,
            self.bar_grey,
            batch=batch
        )

    """Fonction qui met à jour la position en fonction de la vitesse"""

    def aim_at(self, player):
        delta_x = player.x - self.x
        delta_y = player.y - self.y
        self._theta = np.arctan2(delta_y, delta_x)

    def throw_projectile(self):
        speed = self.projectile_speed
        p = Projectile(self.x, self.y, self.speed[0] + speed*np.cos(self._theta), self.speed[1] + speed*np.sin(self._theta), radius=4, color = "r", game_state=self.game_state, ship=None, level=self.level)
        return p
    
    def close_in_and_out(self, player):
        
        self.aim_at(player)

        t = time() - self.old_time
        self.old_time = time()
        
        norme_t1 = np.linalg.norm(self.speed) 
        norme_in_t2 = np.linalg.norm(self.speed + t*self.acceleration*np.array([np.cos(float(self._theta)), np.sin(float(self.theta))]))
        norme_out_t2 = np.linalg.norm(self.speed - t*self.acceleration*np.array([np.cos(float(self._theta)), np.sin(float(self.theta))]))

        distance_player = np.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)

        if (norme_in_t2 <= self.max_speed or norme_in_t2 <= norme_t1) and distance_player > self.engage_radius :
            self.speed += t*self.acceleration*np.array([np.cos(float(self._theta)), np.sin(float(self._theta))])

        if (norme_out_t2 <= self.max_speed or norme_out_t2 <= norme_t1) and distance_player < self.caution_radius :
            self.speed -= t*self.acceleration*np.array([np.cos(float(self._theta)), np.sin(float(self._theta))])

    def tick(self):
        if self.game_state.player.state == "Alive":
            self.aim_at(self.game_state.player)
            P = self.shoot(self.game_state.player)
            if P is not None:
                self.game_state.add_entity(P)

        super().tick()
        self.close_in_and_out(self.game_state.player)

    def shoot(self, player):
        P = None
        r = np.linalg.norm(self.pos - player.pos)
        if r <= self.caution_radius and r >= self.engage_radius:
            if self.reload % self.reload_speed == 0:
                P = self.throw_projectile()
            self.reload += 1
        return P