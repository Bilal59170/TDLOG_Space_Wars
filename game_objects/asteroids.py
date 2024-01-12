from typing import Any
import numpy as np

import sys
sys.path.append("../")

from game_engine import sprites
from game_engine.utils import create_nagon_vertices, draw_bar
from game_engine.config import *

from game_functions import draw_filled_bar

import time

import game_engine.config as config

class Asteroid(sprites.Polygon):


    """
    Classe Asteroid
    Objectif => Implémenter les astéroïdes de façon simple et modulable
    Solution => Sous classer cette classe mère en changeant ses attributs
    
    """

    ###### ATTRIBUTS ######

    size = 100                  # Taille de l'astéroïde
    n_vertices = 8              # Nombre de côté du polygone

    fillColor = (128, 128, 0)   # Couleur à l'intérieur
    edgeColor = (0, 0, 0)       # Couleur du bord
    lineWidth = 5               # Taille de bord

    bar_grey = (128, 128, 128)  # Gris de la barre de vie
    bar_color = (0,128,0)       # Couleur de la barre de vie
    barWidthFactor = .8         # Longueur de la barre de vie (en % de la taille de l'astéroïde)
    barHeight = 16              # Largeur de la barre de vie
    barSpacing = 2              # Largeur de la bordure

    ressources = 10             # XP donnée en tuant l'astéroïde
    max_HP = 100                # PVs maximum de l'astéroïd
    mass = 100
    damage = 100 



    def __init__(self, pos, game_state, theta=0, speed=np.array([0,0])):

        vertices = create_nagon_vertices(self.n_vertices, self.size)
        super().__init__(pos, vertices, game_state, fillColor=self.fillColor, edgeColor=self.edgeColor, lineWidth=self.lineWidth, speed=speed, theta=theta)
        self.orientation = theta

        self._HP = self.max_HP
        self.alive = True

    def tick(self):
        """
        Fonction de tick
            OPTIONNEL => Rajouter la régénération au bout d'un certain temps
        """
        self.speed[0] *= config.ASTEROID_FRICTION
        self.speed[1] *= config.ASTEROID_FRICTION

        super().tick()

    @property
    def HP(self):
        return self._HP

    @HP.setter
    def HP(self, HP):
        if HP <= 0:
            self.die()
        self._HP = min(self.max_HP, HP)


    def draw(self, batch=None):
        """Dessine l'astéroïde"""
        super().draw(batch=batch)

        if self._HP < self.max_HP:
            
            draw_filled_bar(
                pos = (self.screen_pos[0], self.screen_pos[1]-self.size-self.barHeight),
                width = self.size*2*self.barWidthFactor,
                height = self.barHeight,
                spacing = self.barSpacing,
                filled_percent = self._HP/self.max_HP,
                primary_color = self.bar_color,
                secondary_color = self.bar_grey,
                batch=batch
            )


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
        

class MasterAsteroid(Asteroid):   
    size = 100
    n_vertices = 8
    fillColor = (128, 128, 0)
    edgeColor = (0, 0, 0)
    lineWidth = 5

    bar_grey = (128, 128, 128)
    bar_color = (0,128,0)
    barWidthFactor = .8
    barHeight = 16
    barSpacing = 2

    max_HP = 100
    ressources = 100
    mass = 100

class BigAsteroid(Asteroid):
    size = 60
    n_vertices = 5
    fillColor = (118,141,252)
    edgeColor = (88,105,189)
    lineWidth = 5

    bar_color = (118,141,252)

    max_HP = 100
    ressources = 100
    mass = 100

class MediumAsteroid(Asteroid):
    # Astéroïde Triangle !
    size = 30                   # Taille
    n_vertices = 3              # C'est un triangle => 3 côtés
    fillColor = (252,118,119)   # Couleur de remplissage
    edgeColor = (189,88,89)     # Couleur des bords
    lineWidth = 4               # Épaisseur du bord

    bar_grey = (128, 128, 128)  # Fond gris de la barre de vie
    bar_color = (252,118,119)   # Couleur de la barre de vie
    barWidthFactor = .8         # La longueur de la barre de vie (en % de la taille de l'astéroïde)
    barHeight = 16              # La largeur de la barre de vie (en px)
    barSpacing = 3              # Taille de la bordure

    max_HP = 50                 # PVs de l'astéroïde 
    ressources = 50             # Les ressources qu'il donne quand tué
    mass = 50


class SmallAsteroid(Asteroid):
    size = 30
    n_vertices = 4
    fillColor = (255,232,105)
    edgeColor = (191,174,78)

    bar_color = (255,232,105)

    max_HP = 10
    ressources = 10
    mass = 10