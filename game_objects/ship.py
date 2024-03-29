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

from UI import draw_filled_bar, append_new_score
class Ship(sprites.Polygon, pyglet.event.EventDispatcher):
    """ Classe du vaisseau principal """

    

    ship_color = (255,0,0)
    
    bar_grey = (128, 128, 128)  # Gris de la barre de vie
    bar_color = ship_color      # Couleur de la barre de vie
    barWidthFactor = .8         # Longueur de la barre de vie (en % de la taille de l'astéroïde)
    barHeight = 16              # Largeur de la barre de vie
    barSpacing = 2              # Largeur de la bordure
    barwidth = 50               # Longueur de la barre de vie
    is_invicible = False        # Statut d'invincibilité. Obtenu pendant une durée invicible_time quand le joueur touche un astéroïde
    timer_invicible = 0         # Chronometre qui mesure le temps d'invincibilité en seconde
    invicible_time = 1          # La durée d'invincibilité, en seconde
    size = 10                   # Taille du vaisseau: distance des trois sommets par rapport au centre

    reload_speeds = [4, 4, 3, 3]
    size_levels = [6, 8, 10, 12]
    damage_levels = [5, 10, 15, 20]

    def __init__(self, pos, game_state, step=0):
        self.size_step = 10 
        self.acceleration = config.SHIP_ACCELERATION
        self.max_speed = config.SHIP_MAX_SPEED
        self.bullet_speed = 20
        self.max_HP = 2000

        #3 Sommets du triangle
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
        Fonction de mort du vaisseau. On enregistre la dernière position du vaisseau pour le rendre immobile ensuite
        . Avec la position enregistrée, on met une animation sur son lieu de mort (cf game).
        """
        print("MORT DU VAISSEAU")
        self.game_state.player_dead = "Dead"
        self.is_invicible = False
        self.timer_invicible = 0
        return self.pos


    def get_angle_mouse(self):
        """Fonction qui donne l'angle entre la position du vaisseau et celle d'un
        point (x,y)"""
        delta_x = self.game_state.mouse_x - self.screen_x
        delta_y = self.game_state.mouse_y - self.screen_y
        self.theta = np.arctan2(delta_y, delta_x)
    
    @property
    def border(self):
        """Fonction qui sert à gérer les mouvements de la caméra. Exemple: is_border[UP] = True signifie que 
            le vaisseau est trop haut par rapport à la carte pour être au centre de la caméra. Cf game l.480 
            pour voir l'utilisation dans camera"""
        is_border = {'UP': True, 'RIGHT': True,'DOWN': True,'LEFT': True}
        is_border['UP'] = (self.pos[1] - config.WIN_SIZE[1]/2) <= 0
        is_border['DOWN'] = (self.pos[1] + config.WIN_SIZE[1]/2) >= config.MAP_SIZE[1]
        is_border['LEFT'] = (self.pos[0] - config.WIN_SIZE[0]/2) <= 0
        is_border['RIGHT'] = (self.pos[0] + config.WIN_SIZE[0]/2) >= config.MAP_SIZE[0]

        return is_border

    def throw_projectile(self):
        self.get_angle_mouse()
        speed = self.bullet_speed
        p = projectiles.Projectile(self.x, self.y, self.speed[0] + speed*np.cos(self.theta), self.speed[1] + speed*np.sin(self.theta), 4, color = "r", game_state=self.game_state, ship=self, level=self.level)
        return p
    
    def draw(self, batch=None):
        """Dessine l'astéroïde"""
        if self.state == "Alive":
            self.get_angle_mouse()
        super().draw(batch=batch)

        if self.state == "Alive":
            """Dessine la barre de vie"""
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
        self.speed[0] *= config.SHIP_FRICTION
        self.speed[1] *= config.SHIP_FRICTION
        
        if self.state == "Alive":
            super().tick()

            if (self.is_invicible):
                self.timer_invicible += 1/config.TPS
            if self.timer_invicible >= self.invicible_time:
                self.is_invicible = False
                self.timer_invicible = 0


    def update_step(self):
        """Mise à jour de la vitesse du vaisseau. On met une acceleration non nulle."""
        self.level += 1
        self.size_step *= 1.5
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