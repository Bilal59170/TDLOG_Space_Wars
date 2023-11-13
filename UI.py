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


def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


class Sprites:
    def __init__(self, chemin_image=None, polygone=None):
        """
        Classe d'un sprite
        => Implémente les collisions entre sprites
        => Implémente l'affichage sur l'écran
        => Peut être une image ou un polygone
        args : - Nom de fichier
               - Polygone sous forme de liste de points (x, y)
        """
        if chemin_image is not None:
            self.sprite = pyglet.sprite.Sprite(pyglet.image.load(chemin_image))
            self.type = "image"
        elif polygone is not None:
            self.sprite = pyglet.sprite.Sprite(polygone)
            self.type = "polygon"
        else:
            raise ValueError("Il faut un chemin d'image ou un polygone")

    def intersects(self, other):
        match (self.type, other.type):
            case ("image", "image"):
                return self.sprite.intersects(other.sprite)
            case ("image", "polygon"):
                return self.sprite.intersects(other.sprite)
            case ("polygon", "image"):
                return self.sprite.intersects(other.sprite)
            case ("polygon", "polygon"):
                return self.sprite.intersects(other.sprite)
        """Fonction qui calcule si deux sprites se touchent"""


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
        super().__init__(800, 600)  # pos, speed, shape, game_state=None
        self.ship = ship.Ship([400, 300], [10, 10], 1, self)

    """Fonction qui calcule l'angle de visée à chaque déplacement de la souris"""

    def on_mouse_motion(self, x, y, dx, dy):
        self.ship.angle = self.ship.get_angle(x, y)

    def on_draw(self, x, y):
        self.clear()
        self.ship.draw(x, y)


if __name__ == "__main__":
    window = GameWindow()
    pyglet.app.run()
