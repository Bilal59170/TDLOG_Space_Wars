import numpy as np

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

        return x_coordinates, y_coordinates