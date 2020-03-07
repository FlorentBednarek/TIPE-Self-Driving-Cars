import draw
from circuit_arthur import circuit_creation
from classes import *
from NN import Network
import pygame
import time
import random
from evolve import darwin
vector = pygame.math.Vector2


def rand_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


def manual_loop(screen: pygame.Surface, circuit: list, fps_font: pygame.font):
    import settings
    screen_width = settings.screen_size[0]
    clock = pygame.time.Clock()
    dt = 1
    car = Car(circuit, color=pygame.Color(settings.car_color))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill((255, 255, 255))
        draw.circuit(screen, circuit)
        draw.car(screen, [car])
        delta = dt * settings.fps / 1000

        pressed = pygame.key.get_pressed()
        if pressed[settings.left_key]:
            car.abs_rotation -= settings.car_maniability * delta
        if pressed[settings.right_key]:
            car.abs_rotation += settings.car_maniability * delta
        car.apply_vector(car.direction_vector())

        if min(car.position) < 0:
            car.set_position(max(car.position[0], 0),max(car.position[1],0))
        if max(car.position) > screen_width:
            car.set_position(min(car.position[0], screen_width),min(car.position[1],screen_width))
        if not car.detection(screen):
            running = False
            print("MDR T MORT")
        
        draw.fps(screen, fps_font, clock)
        pygame.display.flip()
        dt = clock.tick(settings.fps)

def AI_loop(screen: pygame.Surface, circuit: list, fps_font: pygame.font):
    import settings
    clock = pygame.time.Clock()
    dt = 1
    cars = [Car(circuit, color= rand_color()) for _ in range(settings.cars_number)]
    networks = [Network(c) for c in cars]
    running = True
    
    while running:
        endgen = False
        while not endgen:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            screen.fill((255, 255, 255))
            draw.circuit(screen, circuit)

            draw.car(screen, (net.car for net in networks))

            # Gestion du mouvement de la voiture
            delta = dt * settings.fps / 1000
            if settings.manual_control:
                pass
            else:
                for net in networks:
                    if net.dead == False:
                        net.update()
                        net.car.abs_rotation += settings.car_maniability * delta * net.direction

                        net.car.apply_vector(
                            net.car.direction_vector() * net.engine)
                        if not net.car.detection(screen):
                            net.dead = True

                # alive = 0
                # for net in networks:
                #     if net.dead == 0 :
                #         alive += 1
                if all([x.dead for x in networks]):
                    endgen = True
                    print("MDR PLUS DE VOITURES")
                # for net in networks :
            draw.fps(screen, fps_font, clock)
            pygame.display.flip()
            dt = clock.tick(settings.fps)
        # darwin

        for net in networks:
            net.score = round(vector(net.car.position, [80,130]).length())

        for net in networks:
            net.dead = 0
            net.score = 0
            net.car.position = [80, 130]
            net.car.abs_rotation = 0
        networks = darwin(networks)
        networks = [Network(c) for c in cars]


def main():
    print("""Lancement du programme

    Assurez-vous que toutes les dépendances utilisées soient installées sur votre ordinateur ;
    si besoin entrez `pip install -r requirements.txt` dans votre console
    """)
    pygame.init()
    
    import settings  # doit ABSOLUMENT être appelé *après* le init()
    screen = pygame.display.set_mode(settings.screen_size)
    # screen.fill((255,255,255))
    fps_font = pygame.font.SysFont('Arial', 18)
    pygame.display.set_caption("TIPE")
    # circuit = [Border((10, 10), (10, 100)),
    #             Border((10, 100), (70, 200)),
    #             Border((70, 200), (170, 200))
    #             ]
    circuit = circuit_creation()
    if settings.manual_control:
        # cars = [Car(circuit, color=pygame.Color(settings.car_color), )]
        manual_loop(screen, circuit, fps_font)
    else:
        # cars = [Car(circuit, color= rand_color()) for _ in range(settings.cars_number)]
        # networks = [Network(c) for c in cars]
        AI_loop(screen, circuit, fps_font)
    
    pygame.quit()


if __name__ == "__main__":
    main()
