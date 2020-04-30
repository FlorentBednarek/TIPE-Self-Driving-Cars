import pygame
import time
from math import radians, cos, sin
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


def drawvec(screen: pygame.Surface, car, angle:int, length:int, style: str):
    v = vector(2 * cos(radians(car.abs_rotation + angle)),
            2 * sin(radians(car.abs_rotation + angle)))
    v.scale_to_length(length)
    new_pos = (car.position[0]+v.x,car.position[1]+v.y)
    if style == "Ray":
        pygame.draw.line(screen,car.color, car.position, new_pos, 1)
    elif style == "Cross":
        a = new_pos[0]-5, new_pos[1]-5
        b = new_pos[0]+5, new_pos[1]+5
        c = new_pos[0]-5, new_pos[1]+5
        d = new_pos[0]+5, new_pos[1]-5
        pygame.draw.line(screen,car.color, a, b, 1)
        pygame.draw.line(screen,car.color, c, d, 1)


def general_stats(screen: pygame.Surface, font: pygame.font, clock: pygame.time.Clock, gen_nbr: int, cars_nbr: int, start_time: float):
    texts = list()
    # FPS
    t = clock.get_rawtime()
    nbr = 0 if t==0 else round(1000/t)
    if nbr < 7:
        color = (255, 0, 0)
    elif nbr < 12:
        color = (255, 153, 0)
    else:
        color = (51, 102, 0)
    fps = font.render("FPS: "+str(nbr), True, color, (255,255,255))
    texts.append(fps)
    # Generation Nbr
    if gen_nbr != None:
        generations = font.render("Génération "+str(gen_nbr), True, (0,0,0), (255,255,255))
        texts.append(generations)
    # Alive networks
    if cars_nbr != None:
        s = "s" if cars_nbr>1 else ""
        cars = font.render("{0} voiture{1} restante{1}".format(cars_nbr,s), True, (0,0,0), (255,255,255))
        texts.append(cars)
    # Elapsed time
    t = round(time.time()-start_time,2)
    elapsed_time = font.render("Temps : "+str(t), True, (0,0,0), (255,255,255))
    texts.append(elapsed_time)
    # Display them all
    for e,t in enumerate(texts):
        screen.blit(t, (10, 5+e*15))
    # screen.blit(fps, (10,5))
    # screen.blit(generations, (10,20))
    # screen.blit(cars, (10,35))
    # screen.blit(elapsed_time, (10,50))

def car_specs(screen: pygame.Surface, font: pygame.font, network):
    direction = round(network.direction, 3)
    engine = round(network.engine, 3)
    color = (255,20,20) if network.dead else (0,0,0)
    _, y = screen.get_size()
    # Score
    # score = round(vector(network.car.position, init_pos).length())
    score = network.car.get_score()
    text3 = font.render(f"Score: {score}", True, color, (255,255,255))
    screen.blit(text3, (7,y-50))    
    # Direction
    text1 = font.render(f"Direction: {direction}", True, color, (255,255,255))
    screen.blit(text1, (7,y-35))
    # Vitesse
    text2 = font.render(f"Engine: {engine}", True, color, (255,255,255))
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
            circles.append((screen, circle_color, (x,round(y2)), diam))
            texts.append((font.render(str(round(n.value*1000)), True, text_color, None), (x,y2)))
            temp.append((n, (x,y2)))
            y2 -= diam + 20
        neurons.append(temp)
        x += diam + 80
    for e in range(len(neurons)-1):
        for n1 in neurons[e]:
            for e2, n2 in enumerate(neurons[e+1]):
                n_weight = (n1[0].weight[e2]+2)/4
                color = (round(n_weight*200),)*3
                w = round(n_weight*3)+1
                pygame.draw.line(screen, color, n1[1], n2[1], w)
    for c in circles:
        pygame.draw.circle(*c)
    for text, coo in texts:
        rect = text.get_rect()
        screen.blit(text, (coo[0]-rect.width/2,coo[1]-rect.height/2))