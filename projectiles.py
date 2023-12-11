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
from entity import Entity
import pyglet


class Projectile(Entity):
    """classe projectiles : projectiles circulaires"""

    def __init__(self, x_init, y_init, speed_x_init, speed_y_init, radius, color):
        super().__init__([x_init, y_init], [speed_x_init, speed_y_init])
        self.r = radius
        self.color = color

    def draw(self, batch):
        C = pyglet.shapes.Circle(self.x, self.y, self.r, color = (255, 255, 0), batch=batch)
        C.draw()

    def collision_test():
        """teste si le projectile est en collision à l'instant présent.
        renvoi True s'il y a collision et False sinon"""
        pass

    def is_out(self, x_min, x_max, y_min, y_max):
        if self.x < x_min or self.x > x_max or self.y < y_min or self.y > y_max:
            return True
        return False