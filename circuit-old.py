from math import sqrt, floor
from random import uniform, randint
from classes import Border
import settings


def _ligne_droite(n: int, a: tuple, b: tuple) -> tuple:
    """
    Crée une ligne droite et retourne les bordules du chemin aini que les nouveaux points a et b
    - n (int): nombre de pixels de la ligne droite
    - a et b (tuple de deux entiers): coordonnées du début du chemin
    Retourne : [Bordure 1, Bordure 2, point a, point b]
    """
    taille = settings.screen_size[0]
    x1, x2, y1, y2 = a[0], b[0], a[1], b[1]
    x, y = x1-x2, y1-y2
    if x < 0 and y1 > n:
        return (Border((x1, y1), (x1, y1-n)), Border((x2, y2), (x2, y2-n)), (x1, y1-n), (x2, y2-n))
    if x > 0 and y1 < ((taille/2)-n):
        return (Border((x1, y1), (x1, y1+n)), Border((x2, y2), (x2, y2+n)), (x1, y1+n), (x2, y2+n))
    if y < 0 and x1 > n:
        return (Border((x1, y1), (x1+n, y1)), Border((x2, y2), (x2+n, y2)), (x1+n, y1), (x2+n, y2))
    if y > 0 and x1 < ((taille/2)-n):
        return (Border((x1, y1), (x1-n, y1)), Border((x2, y2), (x2-n, y2)), (x1-n, y1), (x2-n, y2))
    else:
        return(None, None, a, b)


def decoupe(M, i, j):
    A = [[0 for i in range(10)] for j in range(10)]
    #print("Decoupe got i={} j={} (A={}*{} | M={}*{})".format(i,j,len(A),len(A[0]),len(M),len(M[0])))
    for k in range(10):
        for l in range(10):
            A[k][l] = M[k+i][l+j]
    return A


def segmentation():
    """Découpage par bloc l'écran, en 10*10 blocs"""
    n = settings.screen_size[0]
    rep = [[None for _ in range(n)] for _ in range(n)]
    M = [list(range(n)) for j in range(n)]
    for i in range(floor(n*0.9)):
        for j in range(floor(n*0.9)):
            #rep[i][j] = decoupe(M, i, j)
            rep[i][j] = [list(range(x, x+10)) for x in range()]
    return rep


def _virage(d, a, b, taille: int) -> tuple:
    """
    Crée un _virage et retourne les bordules du chemin aini que les nouveaux points a et b
    - d (int): direction du _virage (0=droite,1=gauche)
    - a et b (tuple de deux entiers): coordonnées des bords en entrée de _virage
    Retourne : [Bordure 1, Bordure 2, point a, point b]
    """
    x1, x2, y1, y2 = a[0], b[0], a[1], b[1]
    n = sqrt((x1-x2)**2 + (y1-y2) ** 2)
    x, y = x1-x2, y1-y2
    if d == 0:
        if x < 0:  # renvoie les trait et la position des deux points d'arrivée
            if x2 < int(4*(taille/20)*sqrt(2)/2):
                return (Border((x1, y1), (x1+(3*n/2), y1-(3*n/2))), Border((x2, y2), (x2+(n/2), y2-(n/2))), (x2+(3*n/2), y2-(3*n/2)), (x2+(n/2), y2-(n/2)))
            else:  # si la route est trop pret du bords de l'ecran on fait le virage dans l'autre sens
                return((Border((x1, y1), (x1-(3*n/2), y1-(3*n/2))), Border((x2, y2), (x2-(n/2), y2-(n/2))), (x2-(3*n/2), y2-(3*n/2)), (x2-(n/2), y2-(n/2))))
        if x > 0:
            if x2 > int(4*(taille/20)*sqrt(2)/2):
                return(Border((x1, y1), (x1-(3*n/2), y1+(3*n/2))), Border((x2, y2), (x2-(n/2), y2+(n/2))), (x1-(3*n/2), y1+(3*n/2)), (x2-(n/2), y2+(n/2)))
            else:
                return(Border((x1, y1), (x1+(3*n/2), y1+(3*n/2))), Border((x2, y2), (x2+(n/2), y2+(n/2))), (x1+(3*n/2), y1+(3*n/2)), (x2+(n/2), y2+(n/2)))
        if y < 0:
            if y2 < int(4*(taille/20)*sqrt(2)/2):
                return(Border((x1, y1), (x1-(3*n/2), y1-(3*n/2))), Border((x2, y2), (x2-(n/2), y2-(n/2))), (x1-(3*n/2), y1-(3*n/2)), (x2-(n/2), y2-(n/2)))
            else:
                return(Border((x1, y1), (x1-(3*n/2), y1+(3*n/2))), Border((x2, y2), (x2-(n/2), y2+(n/2))), (x1-(3*n/2), y1+(3*n/2)), (x2-(n/2), y2+(n/2)))
        else:
            if y2 > int(4*(taille/20)*sqrt(2)/2):
                return(Border((x1, y1), (x1+(3*n/2), y1+(3*n/2))), Border((x2, y2), (x2+(n/2), y2+(n/2))), (x1+(3*n/2), y1+(3*n/2)), (x2+(n/2), y2+(n/2)))
            else:
                return(Border((x1, y1), (x1+(3*n/2), y1-(3*n/2))), Border((x2, y2), (x2+(n/2), y2-(n/2))), (x1+(3*n/2), y1-(3*n/2)), (x2+(n/2), y2-(n/2)))
    else:
        if x < 0:
            if x1 > int(4*(taille/20)*sqrt(2)/2):
                return(Border((x1, y1), (x1-(n/2), y1-(n/2))), Border((x2, y2), (x2-(3*n/2), y2-(3*n/2))), (x1-(n/2), y1-(n/2)), (x2-(3*n/2), y2-(3*n/2)))
            else:
                return(Border((x1, y1), (x1+(n/2), y1-(n/2))), Border((x2, y2), (x2+(3*n/2), y2-(3*n/2))), (x2+(n/2), y2-(n/2)), (x2+(3*n/2), y2-(3*n/2)))
        if x > 0:
            if x1 < int(4*(taille/20)*sqrt(2)/2):
                return(Border((x1, y1), (x1+(n/2), y1+(n/2))), Border((x2, y2), (x2+(3*n/2), y2+(3*n/2))), (x1+(n/2), y1+(n/2)), (x2+(3*n/2), y2+(3*n/2)))
            else:
                return(Border((x1, y1), (x1-(n/2), y1+(n/2))), Border((x2, y2), (x2-(3*n/2), y2+(3*n/2))), (x1-(n/2), y1+(n/2)), (x2-(3*n/2), y2+(3*n/2)))
        if y < 0:
            if y1 > int(4*(taille/20)*sqrt(2)/2):
                return(Border((x1, y1), (x1+(n/2), y1-(n/2))), Border((x2, y2), (x2+(3*n/2), y2-(3*n/2))), (x2+(n/2), y2-(n/2)), (x2+(3*n/2), y2-(3*n/2)))
            else:
                return(Border((x1, y1), (x1+(n/2), y1-(n/2))), Border((x2, y2), (x2+(3*n/2), y2-(3*n/2))), (x1+(n/2), y1-(n/2)), (x2+(3*n/2), y2-(3*n/2)))
        else:
            if y1 < int(4*(taille/20)*sqrt(2)/2):
                return(Border((x1, y1), (x1-(n/2), y1+(n/2))), Border((x2, y2), (x2-(3*n/2), y2+(3*n/2))), (x1-(n/2), y1+(n/2)), (x2-(3*n/2), y2+(3*n/2)))
            else:
                return(Border((x1, y1), (x1-(n/2), y1-(n/2))), Border((x2, y2), (x2-(3*n/2), y2-(3*n/2))), (x1-(n/2), y1-(n/2)), (x2-(3*n/2), y2-(3*n/2)))


def circuit_creation(n: int) -> list:
    """
    Crée un circuit avec des bordures
    - n (int): nombre de _virages du circuit
    Retourne: liste de Border
    """
    x1, y1, x2, y2 = 20, 90, 20, 130
    circuit = []
    taille = settings.screen_size[0]
    a, b = [x1, y1], [x2, y2]
    #A = segmentation()
    A = [[None for _ in range(10)] for _ in range(10)]
    for _ in range(n):  # on enchaine ligne droite et virage n fois
        # taille min jusquau prochain bloc et taille max pour pas depasser le suivant
        size_bloc_actuel = round(sqrt( (a[0]-taille/10)**2 + (a[1]-taille/10)**2 ) + 1)
        size_bloc_suivant = round(sqrt( (a[0]-taille/10)**2 + (a[1]-taille/10)**2 ) +taille/10 -1)
        n1 = randint(size_bloc_actuel, size_bloc_suivant)
        circuit += [_ligne_droite(n1, a, b)[0], _ligne_droite(n1, a, b)[1]]
        a, b = _ligne_droite(n1, a, b)[2], _ligne_droite(n1, a, b)[3]
        d = randint(0, 1)
        l1, l2, a, b = _virage(d, a, b, taille)
        x, y = a[0]-b[0], a[1]-b[1]
        case_actuelle = [[a[0]//(taille/10), b[0]//(taille/10)], [a[1]//(taille/10), b[1]//(taille/10)]]
        if x < 0 and y1 > n:
            if A[int(case_actuelle[0][0]+1)][int(case_actuelle[0][1]-1)] != 0:
                circuit += [l1, l2]
                A[int(case_actuelle[0][0]+1)][int(case_actuelle[0][1]-1)] = 0
        if x > 0 and y1 < ((taille/2)-n):
            if A[int(case_actuelle[0][0])][int(case_actuelle[0][1]+1)] != 0:
                circuit += [l1, l2]
                A[int(case_actuelle[0][0])][int(case_actuelle[0][1]+1)] = 0
        if y < 0 and x1 > n:
            if A[int(case_actuelle[1][0]+1)][int(case_actuelle[1][1])] != 0:
                circuit += [l1, l2]
                A[int(case_actuelle[1][0]+1)][int(case_actuelle[1][1])] = 0
        if y > 0 and x1 < ((taille/2)-n):
            if A[int(case_actuelle[1][0]-1)][int(case_actuelle[1][1])] != 0:
                circuit += [l1, l2]
                A[int(case_actuelle[1][0]-1)][int(case_actuelle[1][1])] = 0
    circuit = [x for x in circuit if x!=None]
    return circuit
