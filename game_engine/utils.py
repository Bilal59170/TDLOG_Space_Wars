import numpy as np
import pyglet

def rotate_coordinates(rotation_matrix, coordinates):
    return rotation_matrix @ coordinates

def center_image(image):
    # Sets an image's anchor point to its center
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

def create_nagon_vertices(n, scale, theta = 0):
        angles = np.linspace(0, n, n + 1) / n
        angles = 2 * np.pi * angles[:-1] + theta

        x_coordinates = scale * np.cos(angles)
        y_coordinates = scale * np.sin(angles)

        return np.array([x_coordinates, y_coordinates]).transpose()

def draw_bar(center, width, height, color, batch = None):
    """ Affiche une barre à l'écran. Voir le schéma bar.drawio """
    x, y = center
    r = height/2
    use_batch = batch is None
    if batch is None:
        batch = pyglet.graphics.Batch()
    
    rectangle = pyglet.shapes.Rectangle(x-width/2+r, y-r, width-2*r, 2*r, color=color, batch=batch)
    circle_left = pyglet.shapes.Circle(x-width/2+r, y, r, color=color, batch=batch)
    
    if width > 2*r:
        circle_right = pyglet.shapes.Circle(x+width/2-r, y, r, color=color, batch=batch)

    if not use_batch:
        batch.draw()


import os.path

def func(line):
    return [int(line.split(',')[1]), line.split(',')[0]]

def read_scoreboard(path = "scoreboard.txt"):
    if os.path.isfile(path):
        with open(path, 'r') as fh:
            scores = list(map(func, fh.readlines())) # (score, player)
        
    else:
        with open(path, 'x') as fh:
            scores = [100, 'new user']
    return sorted(scores, key = lambda score : score[0], reverse=True)[:10]

def append_new_score(score, player, path="scoreboard.txt"):
     with open(path, "a") as fh:
          fh.write(str(score) + "," + player)

