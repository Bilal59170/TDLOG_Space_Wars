import numpy as np


try:
    from numba import jit, njit
except:
    jit = lambda x:x
    njit = lambda x:x
    print("Warning: numba not installed, collisions will be slow")

@njit
def lineLineCollision(lineStart1: np.ndarray, lineEnd1: np.ndarray, lineStart2: np.ndarray, lineEnd2: np.ndarray):

    # Si les droites sont parallèles
    denominator = np.cross(lineEnd1 - lineStart1, lineEnd2 - lineStart2)

    if denominator == 0:
        return False

    t = lineEnd1 - lineStart1 / np.linalg.norm(lineEnd1 - lineStart1)
    n = [-t[1], t[0]]

    n1 = np.dot(n, lineStart2-lineStart1)
    n2 = np.dot(n, lineEnd2-lineStart1)

    if n1*n2 > 0:
        return False
    
    return True

"""
@njit
def lineLineCollision(lineStart1: np.ndarray, lineEnd1: np.ndarray, lineStart2: np.ndarray, lineEnd2: np.ndarray):
    # https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
    x1, y1 = lineStart1
    x2, y2 = lineEnd1
    x3, y3 = lineStart2
    x4, y4 = lineEnd2

    denominator = np.cross(lineEnd1 - lineStart1, lineEnd2 - lineStart2)

    
    t = lineStart2 - lineStart1, lineEnd2 - lineStart2) / denominator

    # Si les droites sont parallèles
    if denominator == 0:
        return False

    # Calculate the point of intersection
    x = ((x1 * y2 - y1 * x2) * (x3 - x4) -
         (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
    y = ((x1 * y2 - y1 * x2) * (y3 - y4) -
         (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator

    # Check if the point of intersection is on the line segments
    if x < min(x1, x2) or x > max(x1, x2):
        return False
    if x < min(x3, x4) or x > max(x3, x4):
        return False
    if y < min(y1, y2) or y > max(y1, y2):
        return False
    if y < min(y3, y4) or y > max(y3, y4):
        return False

    return True
"""

@njit
def lineCircleCollision(lineStart: np.ndarray, lineEnd: np.ndarray, circleCenter: np.ndarray, circleRadius: float):
    t = (lineEnd - lineStart) /  np.linalg.norm(lineEnd - lineStart)
    dist = np.cross(circleCenter - lineStart, t)
    return dist < circleRadius

@njit
def polygonCircleCollision(polygonVertices: np.ndarray, circleCenter: np.ndarray, circleRadius: float):
    for i in range(len(polygonVertices)):
        lineStart = polygonVertices[i]
        lineEnd = polygonVertices[(i + 1) % len(polygonVertices)]
        if lineCircleCollision(lineStart, lineEnd, circleCenter, circleRadius):
            return True
    return False

@njit
def circleCircleCollision(circleCenter1: np.ndarray, circleRadius1: float, circleCenter2: np.ndarray, circleRadius2: float):
    return np.linalg.norm(circleCenter1 - circleCenter2) < circleRadius1 + circleRadius2

@njit
def polygonPolygonCollision(polygonVertices1: np.ndarray, polygonVertices2: np.ndarray):

    # Test des coordoonnées pour déterminer si les polygones sont proches
    if np.max(polygonVertices1[:,0]) < np.min(polygonVertices2[:,0]) or np.max(polygonVertices2[:,0]) < np.min(polygonVertices1[:,0]):
        return False
    if np.max(polygonVertices1[:,1]) < np.min(polygonVertices2[:,1]) or np.max(polygonVertices2[:,1]) < np.min(polygonVertices1[:,1]):
        return False

    for i in range(len(polygonVertices1)):
        lineStart = polygonVertices1[i]
        lineEnd = polygonVertices1[(i + 1) % len(polygonVertices1)]
        for j in range(len(polygonVertices2)):
            lineStart2 = polygonVertices2[j]
            lineEnd2 = polygonVertices2[(j + 1) % len(polygonVertices2)]
            if lineLineCollision(lineStart, lineEnd, lineStart2, lineEnd2):
                return True
    return False

@njit
def polygonPolygonCollisionOptimizedV2(polygonVertices1: np.ndarray, polygonVertices2: np.ndarray):
    # Fonctionnement : on projette les polygones sur un axe, et on teste si les projections se superposent
    # Si les projections se superposent pour tous les axes, alors les polygones se superposent

    for polygon in [polygonVertices1, polygonVertices2]:
        for i in range(len(polygon)):
            edge = polygon[i] - polygon[ (i + 1) % len(polygon)]

            n = np.array([edge[1], -edge[0]])
            n /= np.linalg.norm(n)

            dot_product = polygonVertices1 @ n
            min1, max1 = np.min(dot_product), np.max(dot_product)
            
            dot_product = polygonVertices2 @ n
            min2, max2 = np.min(dot_product), np.max(dot_product)

            if max1 < min2 or max2 < min1:
                return False

    return True


def polygonPolygonCollisionOptimized(polygonVertices1: np.ndarray, polygonVertices2: np.ndarray):
    # Fonctionnement : on projette les polygones sur un axe, et on teste si les projections se superposent
    # Si les projections se superposent pour tous les axes, alors les polygones se superposent

    for polygon in [polygonVertices1, polygonVertices2]:
        i = np.arange(len(polygon))
        edges = polygon[i] - polygon[ (i + 1) % len(polygon)] # dims : (n_vertices, 2)

        n = np.array([edges[:, 1], -edges[:,0]])
        n /= np.linalg.norm(n, axis=0)                        # dims : (2, n_vertices_poly_1)

        # Projections des vertices des polygones sur les vecteurs normaux aux côtés
        dot_product = polygonVertices1 @ n # dims : (n_vertices_poly_1, n_vertices_poly_1)

        # Calcul des bornes des projections sur les différents axes; dims : (n_vertices_poly_1)
        min1, max1 = np.min(dot_product, axis=0), np.max(dot_product, axis=0)

        # Projections des vertices des polygones sur les vecteurs normaux aux côtés
        dot_product = polygonVertices2 @ n # dims : (n_vertices_poly_2, n_vertices_poly_1)
        # Calcul des bornes des projections sur les différents axes; dims : (n_vertices_poly_1)
        min2, max2 = np.min(dot_product, axis=0), np.max(dot_product, axis=0)

        if np.any(max1 < min2) or np.any(max2 < min1):
            return False
        
    return True


import threading
import time

def polygon_polygon_collision(polygons):
    """
    Fonction qui teste les collisions entre les polygones de la liste polygons et renvoie les indices de collisions
    """
    indices = []
    for i in range(len(polygons)):
        for j in range(i+1, len(polygons)):
            if polygonPolygonCollision(polygons[i], polygons[j]):
                indices += [(i, j)]

def faster_polygon_polygon_collision(polygons, n_threads = 4):
    """
    Fonction qui teste les collisions entre les polygones de la liste polygons en utilisant le multithreading
    """
    # On crée une liste de threads qui va tester les collisions sur des blocs de polygones
    threads = []
    for i in range(n_threads):
        start = i * len(polygons) // n_threads
        end = (i+1) * len(polygons) // n_threads
        threads += [threading.Thread(target=polygon_polygon_collision, args=(polygons[start:end],))]
    
    # On lance les threads
    for thread in threads:
        thread.start()
    
    # On attend la fin des threads
    for thread in threads:
        thread.join()

    # On récupère les indices de collisions
    indices = []
    for thread in threads:
        indices += thread.result

    return indices


def grid_range(start, stop, grid_size):
    return range(start // grid_size * grid_size, stop, grid_size)    

class GridSpatialPartitioning:
    def __init__(self, cell_size, world_bounds):
        self.cell_size = cell_size
        self.world_bounds = world_bounds
        self.grid = {}

    def insert_into_grid(self, sprite):
        min_x, min_y, max_x, max_y = sprite.bounds
        for x in grid_range(min_x, max_x, self.cell_size):
            for y in grid_range(min_y, max_y, self.cell_size):
                if (x, y) not in self.grid:
                    self.grid[(x, y)] = []
                self.grid[(x, y)].append(sprite)

    def get_potential_collisions(self, sprite):
        potential_collisions = set()
        min_x, min_y, max_x, max_y = sprite.bounds
        for x in grid_range(min_x, max_x, self.cell_size):
            for y in grid_range(min_y, max_y, self.cell_size):
                potential_collisions.update(self.grid.get((x, y), []))
        return potential_collisions

    def check_collisions(self, sprite):
        min_x, min_y, max_x, max_y = sprite.bounds
        for x in grid_range(min_x, max_x):
            for y in grid_range(min_y, max_y):
                if (x, y) in self.grid:
                    other_sprite = self.grid[(x, y)]
                    if sprite.intersects(other_sprite):
                        yield other_sprite

    def check_collisions(self, sprite):
        potential_collisions = self.get_potential_collisions(sprite)
        for other_sprite in potential_collisions:
            if sprite.intersects(other_sprite):
                yield other_sprite


if __name__ == "__main__":
    # Test
    lineStart = np.array([100, 170])
    lineEnd = np.array([276, 50])
    circleCenter = np.array([222, 30])
    radius = 10

    print(lineCircleCollision(lineStart, lineEnd, circleCenter, radius))
