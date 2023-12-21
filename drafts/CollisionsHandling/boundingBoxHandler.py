"""
Ce fichier impémente la classe BoundingBoxHandler qui permet de gérer les collisions entre les entités, ainsi que la classe Rectangle qui représente un rectangle
et que la classe Circle qui représente un cercle

"""
from spatialPartitioning import GridSpatialPartitioning, QuadTreeSpatialPartitioning
from collisions import polygonPolygonCollision


class Rectangle:
    """
    Classe qui représente un rectangle
    """

    def __init__(self, x, y, w, h):
        """
        x, y : coordonnées du coin supérieur gauche du rectangle
        w, h : largeur et hauteur du rectangle
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def contains(self, entity):
        """
        Renvoie True si l'entité est dans le rectangle
        """
        return self.x <= entity.x <= self.x + self.w and self.y <= entity.y <= self.y + self.h
    
    def intersects(self, range):
        """
        Renvoie True si le rectangle intersecte le rectangle range
        """
        return not (range.x > self.x + self.w or range.x + range.w < self.x or range.y > self.y + self.h or range.y + range.h < self.y)

class Circle:
    """
    Classe qui représente un cercle
    """

    def __init__(self, x, y, r):
        """
        x, y : coordonnées du centre du cercle
        r : rayon du cercle
        """
        self.x = x
        self.y = y
        self.r = r
    
    def contains(self, entity):
        """
        Renvoie True si l'entité est dans le cercle
        """
        return (self.x - entity.x)**2 + (self.y - entity.y)**2 <= self.r**2
    
    def intersects(self, other):
        """
        On regarde le type de l'autre objet
        """
        if isinstance(other, Rectangle):
            return self.intersects_rectangle(other)
        elif isinstance(other, Circle):
            return self.intersects_circle(other)
        else:
            raise Exception("Type d'objet non reconnu")
    
    def intersects_rectangle(self, rectangle):
        """
        Renvoie True si le cercle intersecte le rectangle
        """
        # On commence par regarder si le centre du cercle est dans le rectangle
        if rectangle.contains(self):
            return True
        
        # On regarde si le cercle intersecte un des bords du rectangle
        # On commence par regarder si le centre du cercle est dans la bande verticale du rectangle
        if rectangle.x <= self.x <= rectangle.x + rectangle.w:
            # On regarde si le cercle intersecte le bord supérieur ou inférieur du rectangle
            return rectangle.y <= self.y <= rectangle.y + rectangle.h or rectangle.y <= self.y + self.r <= rectangle.y + rectangle.h
        # On regarde si le centre du cercle est dans la bande horizontale du rectangle
        elif rectangle.y <= self.y <= rectangle.y + rectangle.h:
            # On regarde si le cercle intersecte le bord gauche ou droit du rectangle
            return rectangle.x <= self.x <= rectangle.x + rectangle.w or rectangle.x <= self.x + self.r <= rectangle.x + rectangle.w
        else:
            # Le cercle n'intersecte pas le rectangle
            return False
    
    def intersects_circle(self, circle):
        """
        Renvoie True si le cercle intersecte le cercle circle
        """
        return (self.x - circle.x)**2 + (self.y - circle.y)**2 <= (self.r + circle.r)**2
    