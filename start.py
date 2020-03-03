import draw
from circuit_arthur import circuit_creation
from classes import *
from NN import Network
import pygame, time
import random
from evolve import darwin
vector = pygame.math.Vector2

def rand_color():
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    return (r,g,b)

def main():
    print("""Lancement du programme

    Assurez-vous que toutes les dépendances utilisées soient installées sur votre ordinateur ;
    si besoin entrez `pip install -r requirements.txt` dans votre console
    """)

    pygame.init()
    clock = pygame.time.Clock()

    import settings # doit ABSOLUMENT être appelé *après* le init()
    screen = pygame.display.set_mode(settings.screen_size)
    pygame.display.set_caption("TIPE")

    # circuit = [Border((10, 10), (10, 100)),
    #             Border((10, 100), (70, 200)),
    #             Border((70, 200), (170, 200))
    #             ]
    circuit = circuit_creation()
    if settings.manual_control:
        cars = [Car(circuit, color=pygame.Color(settings.car_color), )]
    else:

        cars = [Car(circuit, color = rand_color()) for _ in range(settings.cars_number)]
        networks = [Network(c) for c in cars]
    running = True
    dt = 1
    screen_width = settings.screen_size[0]
    while running:
        endgen = 0
        while not endgen:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((255, 255, 255))
            draw.circuit(screen, circuit)
            draw.car(screen,(net.car for net in networks))



            # Gestion du mouvement de la voiture
            delta = dt * settings.fps / 1000
            if settings.manual_control:
                pressed = pygame.key.get_pressed()

                if pressed[settings.left_key]:
                    cars[0].abs_rotation -= settings.car_maniability * delta
                if pressed[settings.right_key]:
                    cars[0].abs_rotation += settings.car_maniability * delta
                cars[0].apply_vector(cars[0].direction_vector())

                if min(cars[0].position) < 0:
                    cars[0].set_position(max(cars[0].position[0],0),max(cars[0].position[1],0))
                if max(cars[0].position) > screen_width:
                    cars[0].set_position(min(cars[0].position[0],screen_width),min(cars[0].position[1],screen_width))
                if not cars[0].detection(screen):
                    running = False
                    print("MDR T MORT")
                #print(cars[0].position)
            else:
                for net in networks:
                    if net.dead == 0 :
                        net.update()
                        net.car.abs_rotation -= settings.car_maniability * delta * net.direction
                        
                        net.car.apply_vector(net.car.direction_vector())
                        if not net.car.detection(screen):
                            net.dead = 1
                    
                alive = 0
                for net in networks:
                    if net.dead == 0 :
                        alive += 1
                if not alive :
                    endgen = True
                    print("MDR PLUS DE VOITURES")
                for net in networks :
                    pygame.display.flip()
            dt = clock.tick(settings.fps)
        #darwin

        for net in networks:
            net.score = vector(net.car.position,[110,180]).length()

        networks = darwin(networks)
        for net in networks:
            net.dead = 0
            net.score = 0
            net.car.position = [110,180]
            net.car.abs_rotation = 90
    pygame.quit()


if __name__ == "__main__":
    main()
