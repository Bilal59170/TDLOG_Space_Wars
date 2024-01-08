

def grid_range(start, stop, grid_size):
    return range(start // grid_size * grid_size, stop, grid_size)    

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

class Entity:
    """
    Classe qui représente une entité du jeu
    """

    def __init__(self, x, y):
        """
        x, y : coordonnées de l'entité
        """
        self.x = x
        self.y = y
    
    def get_bounding_box(self):
        """
        Renvoie le rectangle qui englobe l'entité
        """
        return Rectangle(self.x, self.y, 1, 1)
    
    def __repr__(self):
        return f"Entity({self.x}, {self.y})"

class GridSpatialPartitioning:
    """
    Classe qui permet le partitionnement spatial des entités du jeu dans un maillage éparse (sparse grid)
    On utilise une table de hachage pour stocker les entités dans des cellules de la grille
    
    Fonctionnement : 
    - On initialise la grille avec une taille de cellule donnée
    - On ajoute les entités dans la grille
    - On peut récupérer les entités qui sont dans une cellule donnée
    - On peut récupérer les entités qui sont dans une cellule donnée et qui sont proches d'une entité donnée
    """

    def __init__(self, grid_size):
        """
        grid_size : taille d'une cellule de la grille
        """
        self.grid_size = grid_size
        self.grid = {}
    
    def add(self, entity):
        """
        Ajoute une entité dans la grille
        """
        # On récupère les coordonnées de la cellule dans laquelle se trouve l'entité
        grid_x, grid_y = self.get_grid_coords(entity.x, entity.y)
        
        # On ajoute l'entité dans la cellule
        if (grid_x, grid_y) not in self.grid:
            self.grid[(grid_x, grid_y)] = []
        self.grid[(grid_x, grid_y)].append(entity)
    
    def get_grid_coords(self, x, y):
        """
        Renvoie les coordonnées de la cellule dans laquelle se trouve le point (x, y)
        """
        return x // self.grid_size, y // self.grid_size
    
    def get_entities_in_cell(self, x, y):
        """
        Renvoie les entités qui sont dans la cellule (x, y)
        """
        return self.grid.get((x, y), [])
    
    def get_entities_in_cell_and_neighbours(self, x, y):
        """
        Renvoie les entités qui sont dans la cellule (x, y) et dans les cellules voisines
        """
        entities = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                entities.extend(self.get_entities_in_cell(x + i, y + j))
        return entities
    
    def get_entities_near_entity(self, entity):
        """
        Renvoie les entités qui sont dans la cellule de l'entité et dans les cellules voisines
        """
        grid_x, grid_y = self.get_grid_coords(entity.x, entity.y)
        return self.get_entities_in_cell_and_neighbours(grid_x, grid_y)
    
    def get_entities_near_point(self, x, y):
        """
        Renvoie les entités qui sont dans la cellule du point et dans les cellules voisines
        """
        grid_x, grid_y = self.get_grid_coords(x, y)
        return self.get_entities_in_cell_and_neighbours(grid_x, grid_y)

class QuadTree:
    """
    QuadTree pour le partitionnement spatial des entités du jeu
    On utilise un arbre pour stocker les entités dans des cellules de la grille
    """

    def __init__(self, boundary, capacity):
        """
        boundary : rectangle qui représente la zone couverte par le quadtree
        capacity : nombre maximum d'entités dans une cellule
        """
        self.boundary = boundary
        self.capacity = capacity
        self.entities = []
        self.divided = False

    def insert(self, entity):
        """
        Ajoute une entité dans le quadtree
        """
        if not self.boundary.contains(entity):
            return False

        if len(self.entities) < self.capacity:
            self.entities.append(entity)
            return True
        else:
            if not self.divided:
                self.subdivide()
            if self.northwest.insert(entity):
                return True
            elif self.northeast.insert(entity):
                return True
            elif self.southwest.insert(entity):
                return True
            elif self.southeast.insert(entity):
                return True
            else:
                return False
    
    def subdivide(self):
        """
        Divise le quadtree en 4 sous-quadtrees
        """
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        nw = Rectangle(x, y, w / 2, h / 2)
        ne = Rectangle(x + w / 2, y, w / 2, h / 2)
        sw = Rectangle(x, y + h / 2, w / 2, h / 2)
        se = Rectangle(x + w / 2, y + h / 2, w / 2, h / 2)

        self.northwest = QuadTree(nw, self.capacity)
        self.northeast = QuadTree(ne, self.capacity)
        self.southwest = QuadTree(sw, self.capacity)
        self.southeast = QuadTree(se, self.capacity)

        self.divided = True
    
    def query(self, range):
        """
        Renvoie les entités qui sont dans le rectangle range
        """
        entities = []
        if not self.boundary.intersects(range):
            return entities
        else:
            for entity in self.entities:
                if range.contains(entity):
                    entities.append(entity)
            if self.divided:
                entities.extend(self.northwest.query(range))
                entities.extend(self.northeast.query(range))
                entities.extend(self.southwest.query(range))
                entities.extend(self.southeast.query(range))
        return entities
    
    def query_near_entity(self, entity):
        """
        Renvoie les entités qui sont dans le rectangle qui englobe l'entité
        """
        return self.query(entity.get_bounding_box())
    
    def query_near_point(self, x, y, w, h):
        """
        Renvoie les entités qui sont dans le rectangle (x, y, w, h)
        """
        return self.query(Rectangle(x, y, w, h))

class QuadTreeSpatialPartitioning:
    """
    Classe qui permet le partitionnement spatial des entités du jeu dans un quadtree
    On utilise un arbre pour stocker les entités dans des cellules de la grille
    
    Fonctionnement : 
    - On initialise le quadtree avec une taille de cellule donnée
    - On ajoute les entités dans le quadtree
    - On peut récupérer les entités qui sont dans un rectangle donné
    - On peut récupérer les entités qui sont dans un rectangle donné et qui sont proches d'une entité donnée
    """

    def __init__(self, boundary, capacity):
        """
        boundary : rectangle qui représente la zone couverte par le quadtree
        capacity : nombre maximum d'entités dans une cellule
        """
        self.quadtree = QuadTree(boundary, capacity)
    
    def add(self, entity):
        """
        Ajoute une entité dans le quadtree
        """
        self.quadtree.insert(entity)
    
    def get_entities_in_range(self, range):
        """
        Renvoie les entités qui sont dans le rectangle range
        """
        return self.quadtree.query(range)
    
    def get_entities_near_entity(self, entity):
        """
        Renvoie les entités qui sont dans le rectangle qui englobe l'entité
        """
        return self.quadtree.query_near_entity(entity)
    
    def get_entities_near_point(self, x, y, w, h):
        """
        Renvoie les entités qui sont dans le rectangle (x, y, w, h)
        """
        return self.quadtree.query_near_point(x, y, w, h)


if __name__ == "__main__":
    # Test de la classe GridSpatialPartitioning
    grid = GridSpatialPartitioning(10)
    grid.add(Entity(0, 0))
    grid.add(Entity(1, 1))
    grid.add(Entity(2, 2))
    grid.add(Entity(3, 3))

    print(grid.get_entities_in_cell(0, 0))
    print(grid.get_entities_in_cell_and_neighbours(0, 0))
    print(grid.get_entities_near_entity(Entity(0, 0)))

    # Test de la classe QuadTreeSpatialPartitioning
    quadtree = QuadTreeSpatialPartitioning(Rectangle(0, 0, 100, 100), 4)
    quadtree.add(Entity(0, 0))
    quadtree.add(Entity(1, 1))
    quadtree.add(Entity(2, 2))
    quadtree.add(Entity(3, 3))

    print(quadtree.get_entities_in_range(Rectangle(0, 0, 10, 10)))
    print(quadtree.get_entities_near_entity(Entity(0, 0)))
    print(quadtree.get_entities_near_point(0, 0, 10, 10))

    
