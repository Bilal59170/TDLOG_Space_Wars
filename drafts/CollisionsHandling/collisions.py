import numpy as np


try:
    from numba import jit, njit
except:
    jit = lambda x:x
    njit = lambda x:x
    print("Warning: numba not installed, collisions will be slow")



def polygonPolygonCollision(polygonVertices1: np.ndarray, polygonVertices2: np.ndarray):

    for polygon in [polygonVertices1, polygonVertices2]:

        edges = polygon - np.roll(polygon, 1, axis=0)

        # Projections des vertices du polygone sur les vecteurs normaux aux côtés (à la norme près du vecteur normal)
        # Taille : (n_vertices_polygon, n_vertices_poly_1)
        projections = np.cross(polygonVertices1, edges, axis=1)

        # Calcul des bornes des projections sur les différents axes; dims : (n_vertices_poly_1)
        min1, max1 = np.min(projections, axis=0), np.max(projections, axis=0)

        projections = np.cross(polygonVertices1, edges, axis=1)
        min2, max2 = np.min(projections, axis=0), np.max(projections, axis=0)

        if np.any(max1 < min2) or np.any(max2 < min1):
            return False
        
    return True


