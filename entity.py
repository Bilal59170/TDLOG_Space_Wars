from config import *
from utils import *

from typing import Any
from abc import ABC, abstractmethod

import numpy as np


class NoGameStateError(Exception):
    """ Exception levée lorsqu'un objet n'a pas d'attribut game_state"""

    def __init__(self, object):
        super().__init__("No game state attributed to : {}".format(object))


class Entity:
    """ 
    Classe entité
    => Justification :
        - Gestion de la position
            => Pour l'affichage à l'écran (screen_pos)
            => Pour le multijoueur
            => Permet de travailler avec les coordonnées de l'entité sans se soucier de leur provenance 
                => compabilité de ce que l'on a développé avec les éléments à rajouter
        - Gestion de la vitesse
            => Permet, pour le multijoueur, d'estimer la position de l'entité à un instant t à partir de sa position ainsi que sa vitesse à un instant t-1
            => Actualisation de la position à chaque tick en fonction de la vitesse
    
    => Fonctionnalités majeures:
        - pos => Position sur la carte de l'objet
        - speed => Vitesse de l'objet
        - screen_pos => Position de l'objet à l'écran
        - tick => Actualisation de la position selon la vitesse
    
    => Fonctionnalités mineures:
        - x, y => Coordonnées x et y de l'objet sur la carte
        - screen_x, screen_y => Coordonnées x et y de l'objet à l'écran

    """

    def __init__(self, pos, game_state, speed = np.array([0, 0])):

        self._pos = np.array(pos).astype(float)
        self.speed = np.array(speed).astype(float)

        self._game_state = game_state
        self.camera = game_state.camera
        self.map = game_state.map

    @property
    def pos(self):
        return np.array(
            [self._pos[0] % self.map.size[0], self._pos[1] % self.map.size[1]] #sorte de tore
        )

    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @property
    def screen_pos(self):
        """

        Dans cette fonction on adresse un problème aux bords. En effet, on pourrait penser que les coordonnées
        à l'écran, c'est juste les coordonnées sur la carte desquelles on retire le point sur lequel est centré
        la caméra. Mais en fait, ça dépend.

        Par exemple, si on imagine un point sur une carte qui est exactement 4 fois plus petite que l'écran latéralement
        et de la même longueur, le point va apparaître 4 fois si on veut une carte parfaitement torique ...

        On part sur le principe que la fenêtre est plus petite que la carte

        """

        # Empêcher le cas où l'écran est plus grand que la map

        pos_0 = (self.pos - self.camera.center).astype(
            int
        )  # Position 1 : Position normale
        pos_1 = (self.pos - self.camera.center + self.camera.size).astype(
            int
        )  # Position 2 : A gauche ou en bas
        x = (
            pos_0[0]
            if abs(pos_0[0] - WIN_SIZE[0] / 2) < abs(pos_1[0] - WIN_SIZE[0] / 2)
            else pos_1[0]
        )
        y = (
            pos_0[1]
            if abs(pos_0[1] - WIN_SIZE[1] / 2) < abs(pos_1[1] - WIN_SIZE[1] / 2)
            else pos_1[1]
        )

        return np.array([x, y]).astype(int)
    
    def tick(self):
        self.pos += self.speed

    """ Propriétés de positions x/y"""

    @property
    def screen_x(self):
        return self.screen_pos[0]

    @property
    def screen_y(self):
        return self.screen_pos[1]

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]


        

