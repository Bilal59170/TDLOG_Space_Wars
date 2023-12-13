from shapely.geometry import Polygon as Poly

from entity import Entity
from pyglet.gl import *
import pyglet

import numpy as np
from config import *

try:
    from numba import njit
except:
    njit = lambda x:x

class Sprites:
    """ 
    Interface pour les sprites
    
    GPT : un sprite est une représentation visuelle d'un élément du jeu, souvent une image ou une animation,
          qui peut être déplacée et manipulée de manière dynamique à l'écran.
    
    """

    def draw(self):
        raise NotImplementedError

    def collides(self, other):
        raise NotImplementedError



######### PARTIE IMAGES #########

# On utilise numba pour gagner en rapidité sur les calculs => on compile en C
@njit
def check_overlap(mask1, mask2, dx, dy):
    """ Fonction qui teste si deux masques se superposent avec un décalage dx, dy """
    height, width = mask1.shape

    for i in range(height):
        for j in range(width):
            new_i = i + dy # Pixel correspondant dans l'autre image
            new_j = j + dx

            if 0 <= new_i < height and 0 <= new_j < width:
                if mask1[i, j] and mask2[new_i, new_j]:
                    return True

    return False

# Compliqué à comprendre, mais permet de récupérer le masque d'une image, ie les pixels qui sont transparents
def get_sprite_mask(sprite):
    img_data = sprite.image.get_image_data()
    if img_data.format == "RGBA":
        i = img_data.get_data('RGBA', sprite.width*4)
        alpha = np.frombuffer(i, dtype=np.uint8)[::4].astype(bool).reshape(sprite.height, sprite.width)[::BITMAP_RATIO, ::BITMAP_RATIO]
    else:
        dims = np.ceil([sprite.width/5, sprite.height/5])
        return np.ones(dims, dtype=bool)
    return alpha

class Image(Entity, Sprites):
    """
    Sprite pour afficher une image

    Implémentations :
     => draw : affiche l'image
     => intersects : teste si l'image se superpose à un autre sprite
     => theta : angle de rotation de l'image

    """
    def __init__(self, pos,
                image,
                game_state,
                theta=None,
                speed = [0, 0],
                use_mask=True,
                rotates_often=True):
        
        super().__init__(pos, speed, game_state)

        self.sprite = pyglet.sprite.Sprite(img=image, x=Entity.screen_x, y=Entity.screen_y, batch=game_state.batch)

        self._theta = 0 if theta is None else theta
        self.sprite.update(rotation=self._theta)
        self.rotates_often = rotates_often

        if self.use_mask:
            self.mask = get_sprite_mask(self.sprite)


    @property
    def theta(self):
        return self._theta
    
    @theta.setter
    def theta(self, theta):
        self._theta = theta
        self.sprite.update(rotation=theta)
        if self.use_mask and not self.rotates_often:
            self.mask = get_sprite_mask(self.sprite)

    def draw(self):
        x, y = self.screen_pos
        self.sprite.update(x, y)


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


######### PARTIE POLYGONES #########

class Polygon(Entity, Sprites):
    """
    Sprite pour afficher un polygone

    Implémentations :
        => draw : affiche le polygone
        => intersects : teste si le polygone se superpose à un autre sprite
        => theta : angle de rotation du polygone

    """
    def __init__(self, pos, vertices, game_state, lineWidth=1, theta=None, fillColor=None, edgeColor=None, speed=[0, 0]):
        
        if fillColor is None and edgeColor is None:
            raise ValueError("Either fillColor or edgeColor must be specified")
        
        Entity.__init__(self, pos, game_state, speed=speed)

        self._vertices = np.array(vertices)

        if theta is not None:
            self._theta = theta
            self.rotation_matrix = np.array([
                [np.cos(theta), np.sin(theta)],
                [-np.sin(theta), np.cos(theta)],
            ])
    
        self.fillColor = fillColor
        self.edgeColor = edgeColor
        self.lineWidth = lineWidth


    @property
    def theta(self):
        return self._theta
    
    @theta.setter
    def theta(self, theta):
        self._theta = theta
        self.rotation_matrix = np.array([
                [np.cos(theta), np.sin(theta)],
                [-np.sin(theta), np.cos(theta)],
            ])

    @property
    def vertices(self):
        if hasattr(self, 'theta'):
            return self.screen_pos + self._vertices @ self.rotation_matrix
        return self.screen_pos + self._vertices

    def polygon(self):
        return Poly((self.pos[:, np.newaxis] + self.vertices).transpose())
    
    def intersects(self, other):
        if isinstance(other, Polygon):
            return self.polygon().intersects(other.polygon())    
        else:
            raise ValueError("Collision not implemented")
    
    def draw(self, batch = None):
        batch = None
        vertices = self.vertices.astype(int)

        useBatch = batch is None

        if batch is None:
            batch = pyglet.graphics.Batch()

        n = len(vertices)

        # Crée un polygone qui est rempli à l'intérieur
        if self.fillColor is not None:
            batch.add(n, pyglet.gl.GL_POLYGON, None,
                            ('v2f', vertices.reshape(-1)),
                            ('c3B', self.fillColor * n))
            
        if self.edgeColor is not None:
             glLineWidth(self.lineWidth)
             batch.add(n, pyglet.gl.GL_LINE_LOOP, None,
                             ('v2f', vertices.reshape(-1)),
                             ('c3B', self.edgeColor * n))

        if useBatch:
            batch.draw()
