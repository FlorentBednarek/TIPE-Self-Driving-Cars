import pygame
import math
import draw
import time
from typing import Optional
from pygame.math import Vector2 as vector
from numpy import arccos, array, dot, pi, cross, array
from numpy.linalg import det, norm


def lineRayIntersectionPoint(rayOrigin: tuple, rayDirection: tuple, point1: tuple, point2: tuple):
    """Donne le vecteur allant de l'origine vers le point d'intersection
    Source: http://bit.ly/2VfSFOV
    Tous les arguments doivent être de la forme (x,y)"""
    # Convert to vectors
    rayOrigin = vector(rayOrigin)
    rayDirection = vector(rayDirection).normalize()
    point1 = vector(point1)
    point2 = vector(point2)

    # Ray-Line Segment Intersection Test in 2D
    # http://bit.ly/1CoxdrG
    v1 = rayOrigin - point1
    v2 = point2 - point1
    v3 = vector([-rayDirection[1], rayDirection[0]])
    try:
        t1 = v2.cross(v1) / v2.dot(v3)
        t2 = v1.dot(v3) / v2.dot(v3)
    except ZeroDivisionError:
        return []
    if t1 >= 0.0 and t2 >= 0.0 and t2 <= 1.0:
        return [rayOrigin + t1 * rayDirection]
    return []


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return []
    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    if x >= min(line1[0][0], line1[1][0]) and x <= max(line1[0][0], line1[1][0]) and y >= min(line2[0][1], line2[1][1]) and y < max(line2[0][1], line2[1][1]):
        return [x, y]
    return []

class Car:
    """Represente une voiture
    color represente la couleur de la voiture, de type pygame.Color"""

    def __init__(self, circuit: list, color: pygame.Color, abs_rotation: float = 0, starting_pos: tuple = (80, 140)):
        """Initialise la voiture
        - circuit (list): liste des bordures du circuit
        - color (pygame.Color): couleur de la voiture [par défaut rouge]
        - abs_rotation (float): rotation par rapport au plan de la voiture [par défaut sud]
        - starting_pos (tuple): position de départ de la voiture en (x,y) [par défaut (80, 140)]"""
        self.color = color
        self.position = list(starting_pos)
        self.init_pos = starting_pos
        self.init_rotation = abs_rotation
        self.abs_rotation = abs_rotation
        self.circuit = circuit[:-1]
        self.last_border = circuit[-1]
        self.start_time = time.time()
        self.death_time = None
        self.distance = 0
        self.rays = [-70, -50, -30, -10, 10, 30, 50, 70] # angle des rayons
        self.rays_length = 80 # longueur des rayons

    @property
    def distances(self):
        return [self.raytrace(angle, self.rays_length, return_real_distance=True) for angle in self.rays]

    def reset(self):
        "Remet à zéro quelques options pour le prochain tour"
        self.start_time = time.time()
        self.death_time = None
        self.distance = 0
        self.position = list(self.init_pos)
        self.abs_rotation = self.init_rotation

    def get_score(self):
        """Calcule le score de la voiture en fonction de la distance parcourue et du temps passé"""
        d = time.time() if self.death_time == None else self.death_time
        s = self.distance - (d-self.start_time)*5
        return round(s)

    def set_position(self, x: int, y: int):
        """Modifie la position absolue de la voiture
        - x (int): nouvelle position de la voiture sur l'axe X (abscisse)
        - y (int): nouvelle position de la voiture sur l'axe Y (ordonnée)"""
        self.position = [x, y]

    def apply_vector(self, vector: pygame.math.Vector2):
        """Applique un vecteur à la position de la voiture
        - vector (Vector): vecteur à appliquer"""
        self.position[0] += vector.x
        self.position[1] += vector.y
        self.distance += vector.length()

    def raytrace(self, angle: int, max_distance: int = 100, use_absolute_angle: bool = False, return_real_distance: bool = False):
        """Vérifie si le rayon d'angle donné rencontre un mur avant une certaine distance
        - angle (int): angle du rayon en degrés, 0 étant l'avant de la voiture
        - max_distance (int): distance maximum à prendre en compte [par défaut 200]
        - use_absolute_angle (bool): si l'angle donné est relatif au plan (1) ou à la voiture (0) [par défaut False]
        - return_real_distance (bool): si la valeur retournée doit être la distance réelle, et non entre 0 et 1 [par défaut False]

        Retourne un float entre 0 et 1, 0 étant une collision immédiate et 1 à la distance maximum, ou -1 si aucune collision"""
        assert all([isinstance(x, Border) for x in self.circuit]
                   ), "La liste du circuit ne doit contenir que des objets de type Border"
        if not use_absolute_angle:
            angle = self.abs_rotation + angle
        angle = math.radians(angle)
        # direction = vector(round(math.cos(angle), 5),
        #                    round(math.sin(angle), 5))
        distances = [line_intersection((self.position, vector(
            2 * math.cos(angle), 2 * math.sin(angle))*2000), (line.start, line.end)) for line in self.circuit]
        distances = [vector(x[0]-self.position[0], x[1]-self.position[1]).length()
                     for x in distances if len(x) != 0]
        if len(distances) == 0:
            return -1
        shortest_distance = min(distances)
        if shortest_distance > max_distance:
            # if return_real_distance:
            #     return -1
            return -1
        if return_real_distance:
            return shortest_distance
        return shortest_distance/max_distance

    def direction_vector(self) -> vector:
        """Renvoie un vecteur unitaire dans la direction de self.abs_rotation"""
        return vector(2 * math.cos(math.radians(self.abs_rotation)),
                      2 * math.sin(math.radians(self.abs_rotation)))

    def detection(self, screen: pygame.Surface, display_rays: Optional[str]) -> bool:
        """Détecte si la voiture est en collision avec une bordure du circuit"""
        for i, a in enumerate(self.distances):
            if a != -1:
                if display_rays != None:
                    draw.drawvec(screen, self, self.rays[i], a, display_rays)
            if a >= 0 and a <= 9:
                return 0
        return self.distance_to_segment(self.last_border.start,self.last_border.end) > 8

    def distance_to_segment(self, start, end) -> float:
        """Retourne la distance la plus petite entre un point et un segment
        - start (tuple): premier point du segment
        - end (tuuple): dernier point du segment
        
        Retourne un float positif ou nul"""
        P, A, B = array(self.position), array(start), array(end)
        if all(A == P) or all(B == P):
            return 0
        if arccos(dot((P - A) / norm(P - A), (B - A) / norm(B - A))) > pi / 2:
            return norm(P - A)
        if arccos(dot((P - B) / norm(P - B), (A - B) / norm(A - B))) > pi / 2:
            return norm(P - B)
        return round(norm(cross(A-B, A-P))/norm(B-A),3)


class Border:
    """Represente une bordure de circuit
    Ligne droite allant de A(x,y) a B(x,y)"""

    def __init__(self, A: tuple, B: tuple, color: pygame.Color):
        assert isinstance(A, (tuple, list)) and isinstance(B, (tuple, list)) and len(
            A) == len(B) == 2, "A et B doivent être des tuples de longueur 2"
        self.color = color
        self.start = A
        self.end = B
