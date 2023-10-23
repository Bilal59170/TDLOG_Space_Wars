"""
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