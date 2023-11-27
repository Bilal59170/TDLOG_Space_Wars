"""
    Scénario d'une partie :
    Génération initiale de terrain (skip for v1)
    Création du personnage joueur
    Affichage de la fenêtre
    game_time = 0

    Boucle principale de jeu (tant que l'utilisateur ne met pas fin au jeu, ou que vaisseau.PV > 0):
    game_time += TICK_TIMESTEP
    récupérer les événements : position de souris, clic
    game.tick() (for all entities in game: entity.tick())
    si game_time % FRAME_TIME == 0:
        affichage
"""
import pyglet
from pyglet.window import key, mouse
from ship import Ship
import numpy as np

# from game import *


# Create a window
window = pyglet.window.Window()

# music = pyglet.resource.media("ost/bgm_forever.mp3")
# music.play()


@window.event
def on_key_press(symbol, modifiers):
    # Move ship
    if symbol == key.Z or symbol == key.UP:
        speed_vect = [0, -1]
        print("Moving up.")
    elif symbol == key.Q or symbol == key.LEFT:
        speed_vect = [-1, 0]
        print("Moving left.")
    elif symbol == key.S or symbol == key.DOWN:
        speed_vect = [0, 1]
        print("Moving down.")
    elif symbol == key.D or symbol == key.RIGHT:
        speed_vect = [1, 0]
        print("Moving right.")
    # ship.move(speed_vect)


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        # Ship.shoot()
        print("The left mouse button was pressed.")


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    # Modify ship orientation
    print(f"Mouse moved. Current coordinates : {x}, {y}")


@window.event
def on_draw():
    # Clear the window
    window.clear()

    # Create a batch to hold our graphics
    # batch = pyglet.graphics.Batch()

    # Draw a red rectangle
    # x, y, width, height = 100, 100, 200, 150
    # radius = 25
    # pyglet.shapes.Circle(x, y, radius, color=(255, 0, 0), batch=batch).draw()

    # Create the ship
    # current_game = Game()
    ship_test = Ship(np.array([100, 100]), np.array([0, 0]), 50)
    ship_test.draw()


# Start the main event loop (+define the tick duration in seconds for update functions)
# pyglet.clock.schedule_interval(update, TICK_TIME)
pyglet.app.run()
