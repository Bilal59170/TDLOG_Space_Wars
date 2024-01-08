"""
Gestion des collisions => - Collisions ligne - ligne
                          - Collisions ligne - cercle
                          - Collisions polygone - cercle
                          - Collisions cercle - cercle
                          - Collisions polygone - polygone

"""
import numpy as np

try:
    from numba import jit, jit
except:
    jit = lambda x:x
    jit = lambda x:x
    print("Warning: numba not installed, collisions will be slow")


@jit
def lineLineCrossing(lineStart1: np.ndarray, lineEnd1: np.ndarray, lineStart2: np.ndarray, lineEnd2: np.ndarray):
    """
    Fonction qui teste si deux droites se croisent
    """

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


#@jit
def lineCircleCrossing(lineStart: np.ndarray, lineEnd: np.ndarray, circleCenter: np.ndarray, circleRadius: float):
    """
    Fonction qui teste si une droite et un cercle se croisent
    """

    t = (lineEnd - lineStart) /  np.linalg.norm(lineEnd - lineStart)
    dist = np.cross(circleCenter - lineStart, t)
    return dist < circleRadius

#@jit
def polygonCircleCrossing(polygonVertices: np.ndarray, circleCenter: np.ndarray, circleRadius: float):
    """
    Fonction qui teste si un polygone et un cercle se croisent
    """
    for i in range(len(polygonVertices)):
        lineStart = polygonVertices[i]
        lineEnd = polygonVertices[(i + 1) % len(polygonVertices)]
        if lineCircleCrossing(lineStart, lineEnd, circleCenter, circleRadius):
            return True
    return False



@jit
def polygonPolygonCrossing(polygonVertices1: np.ndarray, polygonVertices2: np.ndarray):
    """
    Fonction qui teste si deux polygones se croisent
    """
    
    # Test des intersections entre les côtés des polygones
    for i in range(len(polygonVertices1)):
        lineStart = polygonVertices1[i]
        lineEnd = polygonVertices1[(i + 1) % len(polygonVertices1)]
        for j in range(len(polygonVertices2)):
            lineStart2 = polygonVertices2[j]
            lineEnd2 = polygonVertices2[(j + 1) % len(polygonVertices2)]
            if lineLineCrossing(lineStart, lineEnd, lineStart2, lineEnd2):
                return True
    return False

@jit
def polygonPolygonCrossingOptimized(polygonVertices1: np.ndarray, polygonVertices2: np.ndarray) -> bool:
    # On utilise le théorème de séparation des axes
    # Si les polygones ne se superposent pas sur un axe, alors ils ne se superposent pas

    for polygon in [polygonVertices1, polygonVertices2]:

        for i in range(len(polygon)):
            # Pour chaque côté du polygone
            edge = polygon[i] - polygon[ (i + 1) % len(polygon)]

            # On calcule les projections des polygones sur le vecteur normal au côté
            n = np.array([edge[1], -edge[0]])
            n /= np.linalg.norm(n)

            dot_product = polygonVertices1 @ n
            min1, max1 = np.min(dot_product), np.max(dot_product)
            
            dot_product = polygonVertices2 @ n
            min2, max2 = np.min(dot_product), np.max(dot_product)

            # Si les projections ne se superposent pas, alors les polygones ne se superposent pas
            if max1 < min2 or max2 < min1:
                return False

    return True


def polygonPolygonCrossingVectorized(polygonVertices1: np.ndarray, polygonVertices2: np.ndarray):
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


@jit
def is_point_in_polygon(point, polygon):
    """
    Fonction qui teste si un point est dans un polygone
    """
    # On trace une droite horizontale passant par le point et on compte le nombre d'intersections avec les côtés du polygone
    intersections = 0
    for i in range(len(polygon)):
        line_start = polygon[i]
        line_end = polygon[(i+1) % len(polygon)]
        if line_start[1] <= point[1] <= line_end[1] or line_end[1] <= point[1] <= line_start[1]:
            if line_start[0] <= point[0] <= line_end[0] or line_end[0] <= point[0] <= line_start[0]:
                intersections += 1
    return intersections % 2 == 1

@jit
def circleCircleCollision(circleCenter1: np.ndarray, circleRadius1: float, circleCenter2: np.ndarray, circleRadius2: float):
    return np.linalg.norm(circleCenter1 - circleCenter2) < circleRadius1 + circleRadius2

@jit
def does_polygons_collide(polygonVertices1, polygonVertices2):
    """
    Fonction qui teste si deux polygones se superposent
    """
    if polygonPolygonCrossing(polygonVertices1, polygonVertices2):
        return True
    
    for polygon in [polygonVertices1, polygonVertices2]:
        for vertex in polygon:
            if is_point_in_polygon(vertex, polygon):
                return True