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

# Create a window
window = pyglet.window.Window()


@window.event
def on_draw():
    # Clear the window
    window.clear()

    # Create a batch to hold our graphics
    batch = pyglet.graphics.Batch()

    # Draw a red rectangle
    x, y, width, height = 100, 100, 200, 150
    radius = 25
    pyglet.shapes.Circle(x, y, radius, color=(255, 0, 0), batch=batch).draw()


# Start the main event loop
pyglet.app.run()
