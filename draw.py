import pygame
from math import *
vector = pygame.math.Vector2

def circuit(screen: pygame.Surface, circuit: list):
    """Création du circuit sur l'écran
    - screen (pygame.Surface): écran du jeu
    - circuit (list): liste de toutes les bordures (type Border)"""
    for i in circuit:
        pygame.draw.line(screen, i.color, i.start, i.end)


def car(screen: pygame.Surface, cars: list):
    """Dessine les voitures sur le circuit
    - screen (pygame.Surface): écran du jeu
    - cars (list): liste de toutes les voitures (type Car)"""
    for car in cars:
        if not isinstance(car.color, pygame.Color):
            car.color = pygame.Color(car.color)
        A = rotate(car,[car.position[0] - 10, car.position[1] - 7])
        B = rotate(car,[car.position[0] + 10, car.position[1] - 7])
        C = rotate(car,[car.position[0] + 10, car.position[1] + 7])
        D = rotate(car,[car.position[0] - 10, car.position[1] + 7])
        pygame.draw.line(screen, car.color, A, B, 2)
        pygame.draw.line(screen, car.color, B, C, 2)
        pygame.draw.line(screen, car.color, C, D, 2)
        pygame.draw.line(screen, car.color, D, A, 2)


def rotate(car, X:list) -> list:
	"""Applique une rotation à un point selon la position et la rotation de la voiture
	- car (Car): voiture de référence
	- X (tuple): position du point"""
	return [(X[0]-car.position[0])*cos(radians(car.abs_rotation)) - (X[1]-car.position[1])*sin(radians(car.abs_rotation)) + car.position[0],
    (X[1]-car.position[1])*cos(radians(car.abs_rotation)) + (X[0]-car.position[0])*sin(radians(car.abs_rotation)) + car.position[1]]


def drawvec(screen: pygame.Surface, car, angle:int, length:int) :
    v = length * vector(2 * cos(radians(car.abs_rotation + angle)),
            2 * sin(radians(car.abs_rotation + angle)))

    pygame.draw.line(screen,car.color,(car.position[0],car.position[1]),(car.position[0]+v.x,car.position[1]+v.y),2)


def fps(screen: pygame.Surface, font: pygame.font, clock: pygame.time.Clock):
    # nbr = round(clock.get_fps(),3)
    t = clock.get_rawtime()
    nbr = 0 if t==0 else round(1000/t)
    if nbr < 7:
        color = (255, 0, 0)
    elif nbr < 12:
        color = (255, 153, 0)
    else:
        color = (51, 102, 0)
    text = font.render("FPS: "+str(nbr), True, color, (255,255,255))
    screen.blit(text, (10,5))

def gen_nbr(screen: pygame.Surface, font: pygame.font, i: int):
    text = font.render("Génération "+str(i), True, (0,0,0), (255,255,255))
    screen.blit(text, (10,20))

def car_specs(screen: pygame.Surface, font: pygame.font, network):
    direction = round(network.direction, 3)
    engine = round(network.engine, 3)
    _, y = screen.get_size()
    text1 = font.render("Direction: {}".format(direction), True, (0,0,0), (255,255,255))
    screen.blit(text1, (7,y-35))
    text2 = font.render("Engine: {}".format( engine), True, (0,0,0), (255,255,255))
    screen.blit(text2, (7,y-20))

def car_network(screen: pygame.Surface, font: pygame.font, network):
    _, y = screen.get_size()
    x = 25
    diam = 15
    y -= (diam+20)*len(network.I_layer)
    circle_color = (40,40,250)
    text_color = (250, 250, 250)
    circles = list()
    texts = list()
    neurons = list()
    for layer in [network.I_layer, network.layer_2, network.layer_3, network.layer_4]:
        height = (diam+20)*len(layer)
        y2 = y + height/2
        temp = list()
        for n in layer:
            circles.append((screen, circle_color, (x,y2), diam))
            texts.append((font.render(str(round(n.value*1000)), True, text_color, None), (x,y2)))
            temp.append((n, (x,y2)))
            y2 -= diam + 20
        neurons.append(temp)
        x += diam + 50
    for e in range(len(neurons)-1):
        for n1 in neurons[e]:
            for e2, n2 in enumerate(neurons[e+1]):
                n_weight = (n1[0].weight[e2]+2)/4
                color = (round(n_weight*200),)*3
                w = round(n_weight*3)+1
                pygame.draw.line(screen, pygame.Color(color), n1[1], n2[1], w)
    for c in circles:
        pygame.draw.circle(*c)
    for text, coo in texts:
        rect = text.get_rect()
        screen.blit(text, (coo[0]-rect.width/2,coo[1]-rect.height/2))