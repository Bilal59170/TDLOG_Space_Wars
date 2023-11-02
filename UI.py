"""
Interface Graphique du jeu

- Classe intégrant l'interface graphique du jeu
- Comporte différents menus
- Sprites

"""
import pyglet
import ship


class EventManager:
    pass


class Sprites:
    pass


class GameUI:
    pass


class Menu:
    pass


class DiscoverGamesMenu(Menu):
    pass


class LaunchGameMenu(Menu):
    pass


class GameMenu(Menu):
    pass


class PauseMenu(Menu):
    pass


class GameOverMenu(Menu):
    pass


class GameWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(800, 600)
        self.ship = ship.Ship([400, 300])

    """Fonction qui calcule l'angle de visée à chaque déplacement de la souris"""

    def on_mouse_motion(self, x, y, dx, dy):
        self.ship.angle = self.ship.get_angle(x, y)

    def on_draw(self, x, y):
        self.clear()
        self.ship.draw(x, y)


if __name__ == "__main__":
    window = GameWindow()
    pyglet.app.run()
