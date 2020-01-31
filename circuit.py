from math import sqrt
from random import randint
import settings
from classes import Border


PATH_WIDTH = 50

def ligne_droite_old(n,a,b):    #n est le nombre de pixels de la ligne droite, a et b les coordonnées du début de la ligne
    taille = settings.screen_size[0]
    x1,x2,y1,y2 = a[0],b[0],a[1],b[1]
    dx, dy = round(x1-x2), round(y1-y2)
    if dx<0 and y1 > n+PATH_WIDTH:
        new_a = (x1,y1-n)
        new_b = (x2,y2-n)
    elif dx>0 and y1 < taille-(n+PATH_WIDTH):
        new_a = (x1,y1+n)
        new_b = (x2,y2+n)
    elif dy<0 and x1 > n+PATH_WIDTH:
        new_a = (x1+n,y1)
        new_b = (x2+n,y2)
    elif dy>0 and x1 < taille-(n+PATH_WIDTH):
        new_a = (x1-n,y1)
        new_b = (x2-n,y2)
    elif dx<0:
        new_a = (x1,y1-n)
        new_b = (x2,y2-n)
    elif dx>0:
        new_a = (x1,y1+n)
        new_b = (x2,y2+n)
    elif dy<0:
        new_a = (x1+n,y1)
        new_b = (x2+n,y2)
    elif dy>0:
        new_a = (x1-n,y1)
        new_b = (x2-n,y2)
    else:
        print("a = {} | b = {} | dx = {} | dy = {} | n = {}".format(a,b,dx,dy,n))
        return (None,None,a,b)
    return (Border((x1,y1),new_a),Border((x2,y2),new_b),new_a,new_b)

def ligne_droite(n,a,b):    #n est le nombre de pixels de la ligne droite, a et b les coordonnées du début de la ligne
    taille = settings.screen_size[0]
    x1,x2,y1,y2 = a[0],b[0],a[1],b[1]
    dx, dy = round(x1-x2), round(y1-y2)
    if dx<0: # bas
        if y1 > taille-(n+PATH_WIDTH):
            n = taille-PATH_WIDTH - 5
        new_a = (x1,y1+n)
        new_b = (x2,y2+n)
    elif dx>0: # haut
        if y1 > n+PATH_WIDTH:
            n = PATH_WIDTH - 5
        new_a = (x1,y1-n)
        new_b = (x2,y2-n)
    elif dy<0: # gauche
        if x1 < n+PATH_WIDTH:
            n = PATH_WIDTH - 5
        new_a = (x1-n,y1)
        new_b = (x2-n,y2)
    elif dy>0: # droite
        if x1 > taille-(n+PATH_WIDTH):
            n = PATH_WIDTH - 5
        new_a = (x1+n,y1)
        new_b = (x2+n,y2)
    else:
        print("a = {} | b = {} | dx = {} | dy = {} | n = {}".format(a,b,dx,dy,n))
        return (None,None,a,b)
    return (Border((x1,y1),new_a),Border((x2,y2),new_b),new_a,new_b)

#def decoupe(M,i,j):             #decoupage par blocs
#	A=[[0 for i in range(10)] for j in range(10)]
#	for k in range(10):
#		for l in range(10):
#			   A[k][l]=M[k+10*i][l+10*j]
#	return A

def segmentation():
    n=settings.screen_size[0]
    rep = [[1 for _ in range(int(n/10)+2)] for _ in range(int(n/10)+2)]
    for i in range(int(n/10)+2):
        for j in range(int(n/10)+2):
            if (i==0) or (j==0) or (i==int(n/10)+1) or (j==int(n/10)+1):
                rep[i][j]=0
    return rep


def virage(d,a,b):#d est la direction du virage(0=droite,1=gauche) et a et b les coordonnées des bords en entrée de virage
    taille = settings.screen_size[0]
    x1,x2,y1,y2 = a[0],b[0],a[1],b[1]
    n = sqrt((x1-x2)**2+(y1-y2)**2)
    dx, dy = round(x1-x2), round(y1-y2)
    if d == 0:
        if dx<0 :     #renvoie les trait et la position des deux points d'arrivée
            if x2 < int(4*(taille/20)*sqrt(2)/2):
                new_a = (x1-(3*n/2), y1+(3*n/2))
                new_b = (x2-(n/2),   y2+(n/2))
            else:   #si la route est trop pret du bords de l'ecran on fait le virage dans l'autre sens
                new_a = (x1-(3*n/2), y1-(3*n/2))
                new_b = (x2-(n/2),   y2-(n/2))
        if dx>0:
            if x2 > int(4*(taille/20)*sqrt(2)/2):
                new_a = (x1+(3*n/2), y1-(3*n/2))
                new_b = (x2+(n/2),   y2-(n/2))
            else:
                new_a = (x1+(3*n/2), y1+(3*n/2))
                new_b = (x2+(n/2),   y2+(n/2))
        if dy<0:
            if y2 < int(4*(taille/20)*sqrt(2)/2):
                new_a = (x1-(3*n/2), y1-(3*n/2))
                new_b = (x2-(n/2),   y2-(n/2))
            else:
                new_a = (x1+(3*n/2), y1-(3*n/2))
                new_b = (x2+(n/2),   y2-(n/2))
        else :
            if y2 > int(4*(taille/20)*sqrt(2)/2):
                new_a = (x1+(3*n/2), y1+(3*n/2))
                new_b = (x2+(n/2),   y2+(n/2))
            else:
                new_a = (x1-(3*n/2), y1+(3*n/2))
                new_b = (x2-(n/2),   y2+(n/2))
    else :
        if dx<0 :
            if x1 > int(4*(taille/20)*sqrt(2)/2):
                new_a = (x1-(n/2),   y1-(n/2))
                new_b = (x2-(3*n/2), y2-(3*n/2))
            else:
                new_a = (x1-(n/2),   y1+(n/2))
                new_b = (x2-(3*n/2), y2+(3*n/2))
        if dx>0 :
            if x1 < int(4*(taille/20)*sqrt(2)/2):
                new_a = (x1+(n/2),   y1+(n/2))
                new_b = (x2+(3*n/2), y2+(3*n/2))
            else:
                new_a = (x1+(n/2),   y1-(n/2))
                new_b = (x2+(3*n/2), y2-(3*n/2))
        if dy<0 :
            if y1 > int(4*(taille/20)*sqrt(2)/2):
                new_a = (x1-(n/2),   y1+(n/2))
                new_b = (x2-(3*n/2), y2+(3*n/2))
            else:
                new_a = (x1-(n/2),   y1+(n/2))
                new_b = (x2-(3*n/2), y2+(3*n/2))
        else :
            if y1 < int(4*(taille/20)*sqrt(2)/2):
                new_a = (x1+(n/2),   y1-(n/2))
                new_b = (x2+(3*n/2), y2-(3*n/2))
            else:
                new_a = (x1-(n/2),   y1-(n/2))
                new_b = (x2-(3*n/2), y2-(3*n/2))

    return(Border((x1,y1),new_a),Border((x2,y2),new_b),new_a,new_b)


def virage2(a:tuple,b:tuple):
    taille = settings.screen_size[0]
    x1,x2,y1,y2 = a[0],b[0],a[1],b[1]
    dx, dy = round(x1-x2), round(y1-y2)
    if dx<0:
        pass
    elif dx>0:
        pass
    elif dy<0:
        pass
    elif dy>0:
        pass
    return(Border((x1,y1),new_a),Border((x2,y2),new_b),new_a,new_b)

def circuit_creation(n):  # n nombre de virages du circuit
    x1,y1 = 170,100
    x2,y2 = x1+PATH_WIDTH, y1
    circuit = []
    taille = settings.screen_size[0]
    a,b = (x1,y1), (x2,y2)
    A = segmentation()
    for i in range(n):   #on enchaine ligne droite et virage n fois
        print("ligne depuis a =",a," b=",b)
        cst = a[0] - a[0]%taille/10
        case_width = round(taille/10)
        distance_to_case = round(sqrt( (a[0]%case_width-case_width)**2 + (a[1]%case_width-case_width)**2 ))
        n1 = cst+randint(distance_to_case, distance_to_case+round(taille/10)) #taille min jusquau prochain bloc et taille max pour pas depasser le suivant
        new_lines = ligne_droite(n1,a,b)
        circuit += [new_lines[0],new_lines[1]]
        a,b = new_lines[2],new_lines[3]
        a,b = (round(a[0]),round(a[1])), (round(b[0]),round(b[1]))
        d = randint(0,1)
        print("virage depuis a =",a," b =",b)
        l1,l2,a,b = virage(d,a,b)
        a,b = (round(a[0]),round(a[1])), (round(b[0]),round(b[1]))
        x, y = round(a[0]-b[0]), round(a[1]-b[1])
        bloc_actuel = [round(a[0]//(taille/10)), round(a[1]//(taille/10))]
        if x<0:
            if A[bloc_actuel[0]+1][bloc_actuel[1]-1] != 0:
                A[bloc_actuel[0]][bloc_actuel[1]]=0
                circuit += [l1,l2]
        if x>0:
            if A[bloc_actuel[0]][bloc_actuel[1]+1] != 0:
                A[bloc_actuel[0]][bloc_actuel[1]]=0
                circuit += [l1,l2]
        if y<0:
            if A[bloc_actuel[0]+1][bloc_actuel[1]] != 0:
                A[bloc_actuel[0]][bloc_actuel[1]]=0
                circuit += [l1,l2]
        if y>0:
            if A[bloc_actuel[0]-1][bloc_actuel[1]] != 0:
                A[bloc_actuel[0]][bloc_actuel[1]]=0
                circuit += [l1,l2]
    print("\ntaille du circuit:",len(circuit))
    #for x in circuit:
    #    print(x.start,x.end)
    circuit = [x for x in circuit if x!=None]
    return circuit
