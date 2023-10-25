"""
Interface Graphique du jeu

- Classe intégrant l'interface graphique du jeu
- Comporte différents menus


"""
import pyglet
import ship

class GameWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(800, 600)
        self.ship = ship.Ship([400, 300])

    """Fonction qui calcule l'angle de visée à chaque déplacement de la souris"""

    def on_mouse_motion(self, x, y, dx, dy):
        self.ship.angle = self.ship.get_angle(x, y)

    def on_draw(self):
        self.clear()
        self.ship.draw()

if __name__ == "__main__":
    window = GameWindow()
    pyglet.app.run()