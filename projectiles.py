"""
Implémentation d'un projectile

Propriétés d'un projectile :
- Position X, Y sur la carte
- Taille du projectile
- Vitesse du projectile

Méthodes d'un projectile :
- Affichage sur l'UI
- Collision avec un ennemi
- Collision avec un astéroïde


"""

class Projectile:
    """classe projectiles : projectiles circulaires"""


    def __init__(self, x_init, y_init, speed_x_init, speed_y_init, radius, color) :
        self.x = x_init
        self.y = y_init
        self.vx = speed_x_init
        self.vy = speed_y_init
        self.r = radius
        self.color = color

    def tick():
        """fonction update"""
        pass

    def collision_test():
        """teste si le projectile est en collision à l'instant présent.
        renvoi True s'il y a collision et False sinon"""
        pass