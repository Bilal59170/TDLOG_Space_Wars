"""@package docstring
Implémentation d'un projectile, tiré par le vaisseau

Hérite de la classe Entity pour la gestion de la position

Propriétés d'un projectile :
- Taille du projectile
- Combien de temps il reste en jeu (disparaît au bout d'un certain temps)

Méthodes d'un projectile :

- Collision avec un ennemi
    => Détecter quand le projectile touche un ennemi
    => Nom : projectile.collides_with_ennemies(self, game_state)
    => Retourne : Une liste d'ennemis avec lequel le projectile est en collision (vide s'il ne touche rien)
- Collision avec un astéroïde
    => Détecter quand le projectile touche un astéroïde
    => Nom : projectile.collides_with_asteroids(self, game_state)
    => Retourne : Une liste d'ennemis avec lequel l'astéroïde est en collision (vide s'il ne touche rien)

"""

import sys
sys.path.append("../")

from game_engine.sprites import Circle
import pyglet

class Projectile(Circle):

    damage = 5

    """classe projectiles : projectiles circulaires"""

    def __init__(self, x_init, y_init, speed_x_init, speed_y_init, radius, color, game_state):
        super().__init__([x_init, y_init], radius, game_state, speed=[speed_x_init, speed_y_init])
        self.r = radius
        self.color = color

    def draw(self, batch):
        C = pyglet.shapes.Star(self.screen_x, self.screen_y, self.r, self.r/2, 5, 0 , color=(255, 255,0), batch=batch)
        C.anchor_x = self.r
        C.anchor_y = self.r
        C.draw()


    def is_out(self, x_min, x_max, y_min, y_max):
        x, y = self._pos
        if x < x_min or x > x_max or y < y_min or y > y_max:
            return True
        return False
    
    def tick(self):
        super().tick()

        if(self.is_out(0, self.game_state.map_size[0], 0, self.game_state.map_size[1])):
            # Supprime le projectile si il sort de la carte
            self.game_state.remove_entity(self)
            pass