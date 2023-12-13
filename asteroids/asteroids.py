import numpy as np

import sys
 
# setting path
sys.path.append('../TDLOG_Space_Wars')

import sprites
from config import *
from utils import *

import time




class Asteroid(sprites.Polygon):

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

    fillColor = (128, 128, 0)
    edgeColor = (0, 0, 0)
    lineWidth = 5

    bar_grey = (128, 128, 128)
    bar_color = (0,128,0)
    barWidthFactor = .8
    barHeight = 16
    barSpacing = 5

    ressources = 10
    max_HP = 100

    def __init__(self, pos, game_state, theta=0, speed=np.array([0,0])):

        vertices = create_nagon_vertices(self.n_vertices, self.size)
        super().__init__(pos, vertices, game_state, fillColor=self.fillColor, edgeColor=self.edgeColor, lineWidth=self.lineWidth, speed=speed)
        self.orientation = theta

        self._HP = self.max_HP

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
    def HP(self, HP):
        if HP <= 0:
            self.die()
        self._HP = min(self.max_HP, HP)


    def draw(self, batch=None):
        """Dessine l'astéroïde"""
        super().draw(batch=batch)

        draw_bar(
            center = (self.screen_pos[0], self.screen_pos[1]-self.size-self.barHeight),
            width = self.size*2*self.barWidthFactor,
            height = self.barHeight,
            color = self.bar_grey,
            batch=batch
        )

        width = int(self.size * 2 * self.barWidthFactor - self.barSpacing * 2)
        
        draw_bar(
            center = (self.screen_pos[0]- width * (1 - self._HP/self.max_HP)/2, self.screen_pos[1]-self.size-self.barHeight),
            width = width * self._HP/self.max_HP,
            height = self.barHeight - self.barSpacing,
            color = self.bar_color,
            batch=batch
        )
        
       

class BigAsteroid(Asteroid):
    size = 60
    n_vertices = 5
    fillColor = (118,141,252)
    edgeColor = (88,105,189)
    lineWidth = 5

    bar_color = (118,141,252)

    HP = 100
    ressources = 100

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

    #max_HP = 50                 # PVs de l'astéroïde 
    ressources = 50             # Les ressources qu'il donne quand tué


class SmallAsteroid(Asteroid):
    size = 30
    n_vertices = 4
    fillColor = (255,232,105)
    edgeColor = (191,174,78)

    bar_color = (255,232,105)

    HP = 10
    ressources = 10