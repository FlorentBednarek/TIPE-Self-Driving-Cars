import draw
from circuit_arthur import circuit_creation
from classes import Car
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

def calc_starting_pos(pointA, pointB) -> (tuple, float):
    """Calcule la position de départ des voitures, en fonction du circuit"""
    vect = pygame.math.Vector2(pointB[0]-pointA[0], pointB[1]-pointA[1])
    vect.scale_to_length(vect.length()/2)
    new_point = pointA[0]+vect.x, pointA[1]+vect.y
    n = pygame.math.Vector2(-1,0)
    new_angle = vect.angle_to(n)
    return new_point, new_angle

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
            print("Votre voiture a touché un mur - fin de la partie")
        
        draw.fps(screen, fps_font, clock)
        pygame.display.flip()
        dt = clock.tick(settings.fps)

def AI_loop(screen: pygame.Surface, circuit: list, fps_font: pygame.font):
    print("Astuce : Appuyez sur la touche R si une voiture tourne en rond\n")
    import settings
    clock = pygame.time.Clock()
    dt = 1
    # cars = [Car(circuit, color= rand_color()) for _ in range(settings.cars_number)]
    # init_pos = (80,140)
    init_pos, init_angle = calc_starting_pos(circuit["point1"], circuit["point2"])
    cars = [Car(circuit["bordures"], color= "#ff0000", starting_pos=init_pos, abs_rotation=init_angle) for _ in range(settings.cars_number)]
    networks = [Network(c) for c in cars]
    running = True

    increment = 0
    # f = open("car.log", "w")

    def check_events() -> int:
        # 0 - continue
        # 1 - stop gen
        # 2 - stop everything
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 2
            if event.type == pygame.KEYDOWN:
                if event.unicode == "r": # reset:
                    return 1
        return 0
    
    while running:
        increment += 1
        endgen = False
        while not endgen:

            temp = check_events()
            if temp==1:
                endgen = True
                break
            elif temp==2:
                # f.close()
                return
            
            screen.fill((255, 255, 255))
            draw.circuit(screen, circuit["bordures"])

            draw.car(screen, (net.car for net in networks))

            # Gestion du mouvement de la voiture
            delta = dt * settings.fps / 1000
            if settings.manual_control:
                pass
            else:
                # if not networks[0].dead:
                #     f.write("\t\tDirection : {:05f} - Input : {}\n".format(round(networks[0].direction,5), [round(x.value,3) for x in networks[0].I_layer]))
                for net in networks:
                    if net.dead == False:
                        net.update()
                        net.car.abs_rotation += settings.car_maniability * delta * net.direction

                        net.car.apply_vector(
                            net.car.direction_vector() * net.engine * 2)
                        if not net.car.detection(screen):
                            net.dead = True
                            net.car.death_time = time.time()

                if all([x.dead for x in networks]):
                    endgen = True

                # for net in networks :
            networks[0].car.color = "#00FF00"
            draw.fps(screen, fps_font, clock)
            draw.gen_nbr(screen, fps_font, increment)
            draw.car_specs(screen, fps_font, networks[0])
            draw.car_network(screen, fps_font,networks[0])
            pygame.display.flip()
            dt = clock.tick(settings.fps)

        # darwin
        for net in networks:
            net.score = net.car.get_score()
        # f.write("N°{} - score {}\n\t{}\n\t{}\n\t{}\n\t{}\n".format(increment, networks[0].score, networks[0].I_layer,networks[0].layer_2,networks[0].layer_3,networks[0].layer_4))
        average = round(sum([net.score for net in networks])/len(networks))
        print(f"Génération N°{increment} terminée - score moyen : {average}")
        
        for net in networks:
            net.dead = 0
            net.car.position = [80, 130]
            net.car.abs_rotation = 0
            net.car.reset()

        networks = darwin(networks)


def main():
    print("""Lancement du programme

    Assurez-vous que toutes les dépendances utilisées soient installées sur votre ordinateur ;
    si besoin entrez `pip install -r requirements.txt` dans votre console
    """)
    pygame.init()
    
    import settings  # doit ABSOLUMENT être appelé *après* le init()
    screen = pygame.display.set_mode(settings.screen_size)
    fps_font = pygame.font.SysFont('Arial', 18)
    pygame.display.set_caption("TIPE")
    circuit = circuit_creation()

    if settings.manual_control:
        manual_loop(screen, circuit, fps_font)
    else:
        AI_loop(screen, circuit, fps_font)
    
    pygame.quit()


if __name__ == "__main__":
    main()
