"""
Implémentation du vaisseau
Implémentera Entity

"""
import numpy as np
import entity
import pyglet

class Ship(entity.Entity):
    def __init__(self, pos, speed, game_state=None):
        super().__init__(pos, speed, game_state)
        self.angle = 0
    
    """Fonction qui donne l'angle entre la position du vaisseau et celle d'un point (x,y)"""

    def get_angle(self, x, y):
        delta_x = x - self.pos[0]
        delta_y = y - self.pos[1]
        return np.arctan2(delta_y, delta_x)
    
    """On appelle la fonction précédente à chaque mouvement de la souris"""

    @window.event
    def on_mouse_motion(self, x, y, dx, dy):
        self.angle = self.get_angle(x, y)

