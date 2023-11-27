"""
Classe entité, dont hérite les projectiles, astéroïdes, le vaisseau, et les ennemis

Les différentes classes héritant de celle-ci ont toutes diverses méthodes :

- Affichage sur l'UI
    => Nom : display(self, game_state)
- Méthode de tick
    => Nom : tick(self, game_state)


Propriétés :
- Les coordonnées X et Y
- Sa vitesse

Méthodes:
- tick: pour bouger l'entité
- set_game_state : pour attribuer une instance de jeu à l'objet

"""

from config import *

import numpy as np


class NoGameStateError(Exception):
    """Exception levée lorsqu'un objet n'a pas d'attribut game_state"""

    def __init__(self, object):
        super().__init__("No game state attributed to : {}".format(object))


class NullMap:
    def __init__(self):
        self.size = (0, 0)
        self.center = (0, 0)


class Entity:
    def __init__(self, pos, speed, game_state=None):
        self._pos = np.array(pos)
        self.speed = np.array(speed)

        # Peut-être trop générique
        self.has_game_state = False
        if game_state is not None:
            self._game_state = game_state
            self.map = game_state.map
            self.has_game_state = True
        else:
            self.map = NullMap()

    @property
    def pos(self):
        return np.array(
            [self._pos[0] % self.map.size[0], self._pos[1] % self.map.size[1]]
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

        pos_0 = (self.pos - self.map.center).astype(
            int
        )  # Position 1 : Position normale
        pos_1 = (self.pos - self.map.center + self.map.size).astype(
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

    @property
    def game_state(self):
        if self.has_game_state:
            return self._game_state
        raise NoGameStateError(self)

    def tick(self):
        self.pos += self.speed
