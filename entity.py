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

import numpy as np

from config import *


class NoGameStateError(Exception):
    """Exception levée lorsqu'un objet n'a pas d'attribut game_state"""

    def __init__(self, object):
        super().__init__("No game state attributed to : {}".format(object))


class Entity:
    """
    Classe




    """

    def __init__(self, pos, speed, game_state=None):
        self._pos = np.array(pos)
        self._speed = np.array(speed)

        self.has_game_state = False
        if game_state is not None:
            self._game_state = game_state
            self._map = game_state.map
            self.has_game_state = True

    """ ==== PROPRIETES === """

    """ Propriétés sur la position des objets """

    @property
    def pos(self):
        return np.array(
            [self._pos[0] % self.map.size[0], self._pos[1] % self.map.size[1]]
        )

    @property
    def map_pos(self):
        return self.pos

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

    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @map_pos.setter
    def map_pos(self, pos):
        self._pos = pos

    """ Vitesse """

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed

    """ Propriétés de positions x/y"""

    @property
    def screen_x(self):
        return self.screen_pos[0]

    @property
    def screen_y(self):
        return self.screen_pos[1]

    @property
    def map_x(self):
        return self.pos[0]

    @property
    def map_y(self):
        return self.pos[1]

    @property
    def x(self):
        return self.map_x

    @property
    def y(self):
        return self.map_y

    @x.setter
    @map_x.setter
    def x(self, x):
        self._pos[0] = x

    @y.setter
    @map_y.setter
    def y(self, y):
        self._pos[1] = y

    @property
    def game_state(self):
        if self.has_game_state:
            return self._game_state
        raise NoGameStateError(self)

    @property
    def map(self):
        if self.has_game_state:
            return self._map
        raise NoGameStateError(self)

    """ ==== METHODES ==== """

    def tick(self):
        self.pos += self.speed * TICK_TIME * SPEED_FACTOR

    @game_state.setter
    def set_game_state(self, game_state):
        self.has_game_state = True
        self._game_state = game_state
        self._map = self._game_state._map


entity = Entity([0, 0], [0, 0])
entity.map_pos = [1, 2]
print(entity.pos)
