import numpy as np

import sys
 
# setting path
sys.path.append('../TDLOG_Space_Wars')

from entity import *
from config import *
from utils import *

import time

BAR_GREY = (128, 128, 128)
BAR_COLOR = (0,128,0)

class Asteroid(PolygonSprite):

    """
    Asteroid(Entity) :

    Une classe pour créer un astéroïde, sorte de punching ball qui une fois détruit donne des ressources au joueur

    ...

    Attributs
    ----------
    orientation : float
        angle de l'astéroïde
    size : float
        taille de l'astéroïde
    hp : float
        points de vie
    ressources : float
        nombres de ressources que l'astéroïde apporte au joueur
    asteroid_class : int dans [0, 3]
        classe de l'astéroïde
            0 : petit astéroïde, en forme de triangle
            1 : moyen astéroïde, en forme de carré
            2 : grand astéroïde, en forme de pentagone
            3 : giga  astéroïde, en forme d'hexagone

    Méthodes
    --------
    get_polygon(self) : tuple[array]
        retourne un tuple qui contient les coordonnées x, y sur l'écran du polygone
    get_map_polygon(self) : tuple[array]
        retourne un tuple qui contient les coordonnées x, y sur la carte du polygone
    die :
        fait mourir l'astéroïde, donnant des ressources au joueur
    tick :
        pour gérer les déplacements / la régénération des PVs
    ===========
    Hérite de :
    """

    size = 100
    n_vertices = 8
    color = (255, 255, 0)
    ressources = 10
    HP = 100

    def __init__(self, pos, speed, game_state, theta=0):

        vertices = create_nagon_vertices(self.n_vertices, self.size)
        super().__init__(pos, speed, vertices, self.color, game_state=game_state)
        self.orientation = theta

        self._HP = self.HP

    def tick(self):
        """
        Fonction de tick
            OPTIONNEL => Rajouter la régénération au bout d'un certain temps
        """
        super().tick()

    def die(self):
        """Mort de l'astéroïde. Rapporte des ressources au joueur"""
        self.game_instance.remove(self)

    @property
    def HP(self):
        return self._HP

    @HP.setter
    def HP(self, value):
        if value <= 0:
            self.die()
        self._value = value

    def draw(self, batch=None):
        """Dessine l'astéroïde"""
        t = time.time()
        super().draw(batch=batch)
        draw_bar((self.screen_pos[0], self.screen_pos[1]+self.size+ 20), self.size, 20, BAR_GREY, batch=batch)
        draw_bar((self.screen_pos[0], self.screen_pos[1]+self.size+ 20), self.size, 16, BAR_COLOR, batch=batch)
        print(time.time() - t)


class BigAsteroid(Asteroid):
    size = 100
    n_vertices = 8
    color = (128, 128, 0)
    HP = 100
    ressources = 100

class MediumAsteroid(Asteroid):
    size = 50
    n_vertices = 6
    color = (0, 128, 0)
    HP = 50
    ressources = 50

class SmallAsteroid(Asteroid):
    size = 30
    n_vertices = 4
    color = (0, 0, 128)
    HP = 10
    ressources = 10