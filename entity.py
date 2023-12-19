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
        Position à l'écran de l'entité. La carte étant torique, on doit prendre en compte les cas où l'entité est en dehors de l'écran.
        """

        # Position de l'entité sur la carte
        pos = self.pos + self.camera.size / 2

        # Position de la caméra
        camera_pos = self.camera.center

        # Taille de la caméra
        camera_size = self.camera.size

        # Position de l'entité par rapport à la caméra
        screen_pos = pos - camera_pos

        # Si l'entité est en dehors de l'écran
        map_size = self.map.size
        camera_width, camera_height = camera_size
        screen_pos[0] = (screen_pos[0] + map_size[0]) % map_size[0]
        screen_pos[1] = (screen_pos[1] + map_size[1]) % map_size[1]

        return screen_pos
    
    def tick(self):
        self._pos += self.speed

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


        

