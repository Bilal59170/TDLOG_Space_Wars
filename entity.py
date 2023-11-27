"""@package docstring
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


class Entity:
    def __init__(self, pos, speed, game_state=None):
        self._pos = np.array(pos)
        self.speed = np.array(speed)

    @property
    def pos(self):
        return np.array(
            self._pos
        )

    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    def tick(self):
        self.pos += self.speed

class Sprites(ABC):
    """ Interface pour les sprites """
    @abstractmethod
    def draw(self):
        pass
    @abstractmethod
    def intersects(self, other):
        pass

# On utilise numba pour gagner en rapidité
@njit
def check_overlap(mask1, mask2, dx, dy):
    """Fonction qui teste si deux masques se superposent avec un décalage dx, dy. Un masque est une représentation d'image noir et blanc
    où le noir correspond à la présence d'image et le blanc à l'absence d'image (exemple des images .png)"""
    height, width = mask1.shape

    for i in range(height):
        for j in range(width):
            new_i = i + dy # pixel correspondant dans l'autre image
            new_j = j + dx

            if 0 <= new_i < height and 0 <= new_j < width:
                if mask1[i, j] and mask2[new_i, new_j]:
                    return True

    return False

def get_sprite_mask(sprite):
    img_data = sprite.image.get_image_data()
    if img_data.format == "RGBA":
        i = img_data.get_data('RGBA', sprite.width*4)
        alpha = np.frombuffer(i, dtype=np.uint8)[::4].astype(bool).reshape(sprite.height, sprite.width)[::BITMAP_RATIO, ::BITMAP_RATIO]
    else:
        dims = np.ceil([sprite.width/5, sprite.height/5])
        return np.ones(dims, dtype=bool)
    return alpha

class BitmapSprite(Entity, Sprites):
    """Sprite qui représente une Image. (pas un polygone par exemple)"""
    def __init__(self, pos, speed,
                 image,
                 theta=None,
                 game_state=None,
                 use_mask=True,
                 rotates_often=True):
        
        super().__init__(pos, speed, game_state=game_state)
        
        if game_state is not None:
            self.sprite = pyglet.sprite(image, x=Entity.screen_x, y=Entity.screen_y, batch=game_state.batch)
            self.inBatch = True
        else:
            self.sprite = pyglet.sprite(image, x=Entity.screen_x, y=Entity.screen_y)
            self.inBatch = False

        self._theta = 0 if theta is None else theta
        self.sprite.update(rotation=self._theta)
        self.rotates_often = rotates_often

        if self.use_mask:
            self.mask = get_sprite_mask(self.sprite)
 

    @property
    def theta(self):
        return self._theta
    
    @theta.setter
    def set_theta(self, theta):
        self._theta = theta
        self.sprite.update(rotation=theta)
        if self.use_mask and not self.rotates_often:
            self.mask = get_sprite_mask(self.sprite)

    def draw(self):
        x, y = self.screen_pos
        self.sprite.update(x, y)
        if not self.inBatch:
            self.draw()

    def intersects(self, other):

        if not (self.screen_x < other.screen_x + other.sprite.width and
            self.screen_x + self.sprite.width > other.screen_x and
            self.screen_y < other.screen_y + other.sprite.height and
            self.screen_y + self.sprite.height > other.screen_y):
            return False  # Bounding boxes do not overlap
        
        if not self.use_mask:
            return True
        
        if self.use_mask and self.rotates_often:
            self.mask = get_sprite_mask(self.sprite)
        
        dx = int((self.screen_x - other.screen_x)/BITMAP_RATIO)
        dy = int((self.screen_y - other.screen_y)/BITMAP_RATIO)

        return check_overlap(self.mask, other.mask, dx, dy)


class PolygonSprite(Entity, Sprites):
    def __init__(self, pos, speed, vertices, color, game_state=None, theta=None):
        Entity.__init__(self, pos, speed, game_state=game_state)
        self._vertices = np.array(vertices)
        self.color = color
        if theta is not None:
            self._theta = theta
            self.rotation_matrix = np.array([
                [np.cos(np.pi / 2 - theta), np.sin(np.pi / 2 - theta)],
                [-np.sin(np.pi / 2 - theta), np.cos(np.pi / 2 - theta)],
            ])
    
    @property
    def theta(self):
        return self._theta
    @theta.setter
    def set_theta(self, theta):
        self._theta = theta
        self.rotation_matrix = np.array([
                [np.cos(np.pi / 2 - theta), np.sin(np.pi / 2 - theta)],
                [-np.sin(np.pi / 2 - theta), np.cos(np.pi / 2 - theta)],
            ])
    

    @property
    def vertices(self):
        if hasattr(self, 'theta'):
            return self.screen_pos + self.rotation_matrix @ self._vertices
        return self.screen_pos[:, np.newaxis] + self._vertices

    @property
    def polygon(self):
        return Poly((self.pos[:, np.newaxis] + self.vertices).transpose)
    
    def intersects(self, other):
        if isinstance(other, PolygonSprite):
            return self.polygon.intersects(other.polygon)    
        else:
            raise ValueError("Collision not implemented")
    
    def draw(self):
        pyglet.gl.glColor3ub(*self.color)
        vertices = self.vertices
        pyglet.graphics.draw(len(vertices),
                             pyglet.gl.GL_POLYGON,
                             ('v2f', (self.screen_pos + vertices).reshape(-1)),
                             ('c3B', self.color * len(vertices)))

def nagonSprite(n, scale, color, theta=0):
    pos = [0, 0]
    speed = [0, 0]
    vertices = create_nagon_vertices(n, scale, theta = theta)
    
    return PolygonSprite(pos, speed, vertices, color)
