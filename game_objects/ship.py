""" Classe du vaisseau principal """

import sys
sys.path.append("../")

import numpy as np
import pyglet

from game_engine import config, sprites, entity
from game_objects import projectiles
from game_engine import config
from game_engine.utils import create_nagon_vertices, draw_bar

import game_engine.config as config

from game_functions import draw_filled_bar

class Ship(sprites.Polygon, pyglet.event.EventDispatcher):
    """ Classe du vaisseau principal """

    
    """
    size = 10 # Taille du vaisseau
    acceleration = config.SHIP_ACCELERATION
    max_speed = config.SHIP_MAX_SPEED
    bullet_speed = 20
    max_HP = 1000
    """
    ship_color = (255,0,0)
    
    bar_grey = (128, 128, 128)  # Gris de la barre de vie
    bar_color = ship_color      # Couleur de la barre de vie
    barWidthFactor = .8         # Longueur de la barre de vie (en % de la taille de l'astéroïde)
    barHeight = 16              # Largeur de la barre de vie
    barSpacing = 2              # Largeur de la bordure
    barwidth = 50               # Longueur de la barre de vie
    is_invicible = False
    timer_invicible = 0
    invicible_time = 3          #In seconds
    size = 10

    reload_speeds = [2, 2, 1, 1]

    def __init__(self, pos, game_state, step=0):
        self.size_step = 10 # Taille du vaisseau
        self.acceleration = config.SHIP_ACCELERATION
        self.max_speed = config.SHIP_MAX_SPEED
        self.bullet_speed = 20
        self.max_HP = 1000

        V1 = np.array([0, Ship.size])
        V2 = - Ship.size * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])
        V3 = Ship.size * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])

        vertices = np.array([V1, V2, V3]).astype(int)
        self._vertices = np.array([V1, V2, V3]).astype(int)

        sprites.Polygon.__init__(self, pos, vertices, game_state, fillColor=Ship.ship_color)
        pyglet.event.EventDispatcher.__init__(self)

        self._HP = self.max_HP
        self.xp = 0
        self.level = 0
        self.reload = 0

        self.state = "Alive"

    @property
    def HP(self):
        return self._HP

    @HP.setter
    def HP(self, HP):
        if HP <= 0:
            self.die()
        self._HP = min(self.max_HP, HP)


    def die(self):
        """
        Fonction de mort du vaisseau. On enregistre la dernière position du vaisseau 
        puis on le supprime de l'instance de jeu. Avec la position enregistrée, on 
        met une animation sur son lieu de mort.
        """
        print("MORT DU VAISSEAU")
        self.game_state.player_dead = "Dead"
        return self.pos


    def get_angle_mouse(self):
        """Fonction qui donne l'angle entre la position du vaisseau et celle d'un
        point (x,y)"""
        delta_x = self.game_state.mouse_x - self.screen_x
        delta_y = self.game_state.mouse_y - self.screen_y
        self.theta = np.arctan2(delta_y, delta_x)
    
    @property
    def border(self):
        is_border = {'UP': True, 'RIGHT': True,'DOWN': True,'LEFT': True}
        is_border['UP'] = (self.pos[1] - config.WIN_SIZE[1]/2) <= 0
        is_border['DOWN'] = (self.pos[1] + config.WIN_SIZE[1]/2) >= config.MAP_SIZE[1]
        is_border['LEFT'] = (self.pos[0] - config.WIN_SIZE[0]/2) <= 0
        is_border['RIGHT'] = (self.pos[0] + config.WIN_SIZE[0]/2) >= config.MAP_SIZE[0]

        return is_border

    def throw_projectile(self):
        self.get_angle_mouse()
        speed = self.bullet_speed
        p = projectiles.Projectile(self.x, self.y, speed*np.cos(self.theta), speed*np.sin(self.theta), 4, color = "r", game_state=self.game_state, ship=self, level=self.level)
        return p
    
    def draw(self, batch=None):
        """Dessine l'astéroïde"""
        if self.state == "Alive":
            self.get_angle_mouse()
        super().draw(batch=batch)

        if self.state == "Alive":

            draw_filled_bar(
                pos = (self.screen_pos[0], self.screen_pos[1]-self.size_step-self.barHeight),
                width = self.barwidth, 
                height = self.barHeight,
                spacing = self.barSpacing,
                filled_percent = self._HP/self.max_HP,
                primary_color = self.bar_color,
                secondary_color = self.bar_grey,
                batch=batch
            )

    def tick(self):
        """Fonction qui met à jour la position en fonction de la vitesse"""
        if self.state == "Alive":
            super().tick()

            if (self.is_invicible):
                self.timer_invicible += 1/config.TPS
            if self.timer_invicible >= self.invicible_time:
                self.is_invicible = False
                self.timer_invicible = 0


    def update_step(self):
        self.level += 1
        self.size_step *= 2
        self.max_speed *= 1.2
        self.acceleration *= 1.2
        self.max_HP *= 1.2
        self._HP = self.max_HP

        v1 = np.array([0, self.size_step])
        v2 = - self.size_step * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])
        v3 = self.size_step * np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])
        self._vertices = np.array([v1, v2, v3]).astype(int)

    def shoot(self):
        P = None
        if self.reload % self.reload_speeds[self.level] == 0:
            P = self.throw_projectile()
        self.reload += 1
        return P