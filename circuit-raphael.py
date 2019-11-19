from math import sqrt
from random import randint
import settings
from classes import Border


def ligne_droite(n,a,b):    #n est le nombre de pixels de la ligne droite, a et b les coordonnées du début de la ligne
    taille=settings.screen_size[0]
    x1,x2,y1,y2=a[0],b[0],a[1],b[1]
    x,y=x1-x2,y1-y2
    print(x,y)
    if x<0 and y1>n:
        return(Border((x1,y1),(x1,y1-n)),Border((x2,y2),(x2,y2-n)),(x1,y1-n),(x2,y2-n))
    if x>0 and y1<((taille/2)-n):
        return(Border((x1,y1),(x1,y1+n)),Border((x2,y2),(x2,y2+n)),(x1,y1+n),(x2,y2+n))
    if y<0 and x1>n:
        return(Border((x1,y1),(x1+n,y1)),Border((x2,y2),(x2+n,y2)),(x1+n,y1),(x2+n,y2))
    if y>0 and x1<((taille/2)-n):
        return(Border((x1,y1),(x1-n,y1)),Border((x2,y2),(x2-n,y2)),(x1-n,y1),(x2-n,y2))
    if x<0:
        return(Border((x1,y1),(x1,y1-n)),Border((x2,y2),(x2,y2-n)),(x1,y1-n),(x2,y2-n))
    if x>0:
        return(Border((x1,y1),(x1,y1+n)),Border((x2,y2),(x2,y2+n)),(x1,y1+n),(x2,y2+n))
    if y<0:
        return(Border((x1,y1),(x1+n,y1)),Border((x2,y2),(x2+n,y2)),(x1+n,y1),(x2+n,y2))
    if y>0:
        return(Border((x1,y1),(x1-n,y1)),Border((x2,y2),(x2-n,y2)),(x1-n,y1),(x2-n,y2))
    else:
        print("retourne none")
        return(None,None,a,b)

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


def virage(d,a,b):#d est la direction du virage(0=droite,1=gauche) et a  et b les coordonnées des bords en entrée de virage
    taille=settings.screen_size[0]
    x1,x2,y1,y2=a[0],b[0],a[1],b[1]
    n=sqrt((x1-x2)**2+(y1-y2)**2)
    x,y=x1-x2,y1-y2
    if d == 0:
        if x<0 :     #renvoie les trait et la position des deux points d'arrivée
            if x2<int(4*(taille/20)*sqrt(2)/2):
                return (Border((x1,y1),(x1+(3*n/2),y1-(3*n/2))),Border((x2,y2),(x2+(n/2),y2-(n/2))),(x2+(3*n/2),y2-(3*n/2)),(x2+(n/2),y2-(n/2)))
            else:   #si la route est trop pret du bords de l'ecran on fait le virage dans l'autre sens
                return((Border((x1,y1),(x1-(3*n/2),y1-(3*n/2))),Border((x2,y2),(x2-(n/2),y2-(n/2))),(x2-(3*n/2),y2-(3*n/2)),(x2-(n/2),y2-(n/2))))
        if x>0 :
            if x2>int(4*(taille/20)*sqrt(2)/2):
                return(Border((x1,y1),(x1-(3*n/2),y1+(3*n/2))),Border((x2,y2),(x2-(n/2),y2+(n/2))),(x1-(3*n/2),y1+(3*n/2)),(x2-(n/2),y2+(n/2)))
            else :
                return(Border((x1,y1),(x1+(3*n/2),y1+(3*n/2))),Border((x2,y2),(x2+(n/2),y2+(n/2))),(x1+(3*n/2),y1+(3*n/2)),(x2+(n/2),y2+(n/2)))
        if y<0 :
            if y2<int(4*(taille/20)*sqrt(2)/2):
                return(Border((x1,y1),(x1-(3*n/2),y1-(3*n/2))),Border((x2,y2),(x2-(n/2),y2-(n/2))),(x1-(3*n/2),y1-(3*n/2)),(x2-(n/2),y2-(n/2)))
            else:
                return(Border((x1,y1),(x1-(3*n/2),y1+(3*n/2))),Border((x2,y2),(x2-(n/2),y2+(n/2))),(x1-(3*n/2),y1+(3*n/2)),(x2-(n/2),y2+(n/2)))
        else :
            if y2>int(4*(taille/20)*sqrt(2)/2):
                return(Border((x1,y1),(x1+(3*n/2),y1+(3*n/2))),Border((x2,y2),(x2+(n/2),y2+(n/2))),(x1+(3*n/2),y1+(3*n/2)),(x2+(n/2),y2+(n/2)))
            else:
                return(Border((x1,y1),(x1+(3*n/2),y1-(3*n/2))),Border((x2,y2),(x2+(n/2),y2-(n/2))),(x1+(3*n/2),y1-(3*n/2)),(x2+(n/2),y2-(n/2)))
    else :
        if x<0 :
            if x1>int(4*(taille/20)*sqrt(2)/2):
                return(Border((x1,y1),(x1-(n/2),y1-(n/2))),Border((x2,y2),(x2-(3*n/2),y2-(3*n/2))),(x1-(n/2),y1-(n/2)),(x2-(3*n/2),y2-(3*n/2)))
            else:
                return(Border((x1,y1),(x1+(n/2),y1-(n/2))),Border((x2,y2),(x2+(3*n/2),y2-(3*n/2))),(x2+(n/2),y2-(n/2)),(x2+(3*n/2),y2-(3*n/2)))
        if x>0 :
            if x1<int(4*(taille/20)*sqrt(2)/2):
                return(Border((x1,y1),(x1+(n/2),y1+(n/2))),Border((x2,y2),(x2+(3*n/2),y2+(3*n/2))),(x1+(n/2),y1+(n/2)),(x2+(3*n/2),y2+(3*n/2)))
            else:
                return(Border((x1,y1),(x1-(n/2),y1+(n/2))),Border((x2,y2),(x2-(3*n/2),y2+(3*n/2))),(x1-(n/2),y1+(n/2)),(x2-(3*n/2),y2+(3*n/2)))
        if y<0 :
            if y1>int(4*(taille/20)*sqrt(2)/2):
                return(Border((x1,y1),(x1+(n/2),y1-(n/2))),Border((x2,y2),(x2+(3*n/2),y2-(3*n/2))),(x2+(n/2),y2-(n/2)),(x2+(3*n/2),y2-(3*n/2)))
            else:
                return(Border((x1,y1),(x1+(n/2),y1-(n/2))),Border((x2,y2),(x2+(3*n/2),y2-(3*n/2))),(x1+(n/2),y1-(n/2)),(x2+(3*n/2),y2-(3*n/2)))
        else :
            if y1<int(4*(taille/20)*sqrt(2)/2):
                return(Border((x1,y1),(x1-(n/2),y1+(n/2))),Border((x2,y2),(x2-(3*n/2),y2+(3*n/2))),(x1-(n/2),y1+(n/2)),(x2-(3*n/2),y2+(3*n/2)))
            else:
                return(Border((x1,y1),(x1-(n/2),y1-(n/2))),Border((x2,y2),(x2-(3*n/2),y2-(3*n/2))),(x1-(n/2),y1-(n/2)),(x2-(3*n/2),y2-(3*n/2)))

def circuit_creation(n):  # n nombre de virages du circuit
    x1,y1,x2,y2=100,170,100,210
    circuit=[]
    taille=settings.screen_size[0]
    a,b=[x1,y1],[x2,y2]
    A=segmentation()
    for i in range(n):   #on enchaine ligne droite et virage n fois
        borne1 = int(sqrt( (a[0]-taille/10)**2 + (a[1]-taille/10)**2 )+1)
        borne2 = int(sqrt( ((a[0]-taille/10))**2 + ((a[1]-taille/10))**2 ) -1 + taille/10)
        n1=randint(borne1, borne2) #taille min jusquau prochain bloc et taille max pour pas depasser le suivant
        circuit+=[ligne_droite(n1,a,b)[0],ligne_droite(n1,a,b)[1]]
        a,b=ligne_droite(n1,a,b)[2],ligne_droite(n1,a,b)[3]
        d=randint(0,1)
        l1,l2,a,b=virage(d,a,b)
        x,y=a[0]-b[0],a[1]-b[1]
        bloc_actuel = [int(a[0]//(taille/10)), int(a[1]//(taille/10))]
        if x<0:
            if A[bloc_actuel[0]+1][bloc_actuel[1]-1] != 0:
                A[bloc_actuel[0]][bloc_actuel[1]]=0
                circuit+=[l1,l2]
        if x>0:
            if A[bloc_actuel[0]][bloc_actuel[1]+1] != 0:
                A[bloc_actuel[0]][bloc_actuel[1]]=0
                circuit+=[l1,l2]
        if y<0:
            if A[bloc_actuel[0]+1][bloc_actuel[1]] != 0:
                A[bloc_actuel[0]][bloc_actuel[1]]=0
                circuit+=[l1,l2]
        if y>0:
            if A[bloc_actuel[0]-1][bloc_actuel[1]] != 0:
                A[bloc_actuel[0]][bloc_actuel[1]]=0
                circuit+=[l1,l2]
    circuit = [x for x in circuit if x!=None]
    return circuit
