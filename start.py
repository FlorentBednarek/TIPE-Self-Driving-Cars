import draw
from circuit_arthur import circuit_creation
from classes import Car
from NN import Network
from configManager import Config, load_from_filename
import pygame
import time
import random
from evolve import darwin

vector = pygame.math.Vector2
SETTINGS: Config = None
fps = 20


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
    n = pygame.math.Vector2(0, 1)
    new_angle = -round(vect.angle_to(n))
    vect = vect.rotate(-90)
    vect.scale_to_length(20)
    new_point = new_point[0]+vect.x, new_point[1]+vect.y
    return new_point, new_angle


def manual_loop(screen: pygame.Surface, circuit: list, fps_font: pygame.font):
    screen_width = SETTINGS.screen_size[0]
    clock = pygame.time.Clock()
    dt = 1
    color = pygame.Color(SETTINGS.car_color)
    init_pos, init_angle = calc_starting_pos(circuit["point1"], circuit["point2"])
    car = Car(circuit["bordures"], color=color, starting_pos=init_pos,
                abs_rotation=init_angle)
    running = True
    start_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill(SETTINGS.colors["background"])
        draw.circuit(screen, circuit["bordures"])
        draw.car(screen, [car])
        delta = dt * fps / 1000

        pressed = pygame.key.get_pressed()
        if pressed[SETTINGS.left_key]:
            car.abs_rotation -= SETTINGS.car_maniability * delta
        if pressed[SETTINGS.right_key]:
            car.abs_rotation += SETTINGS.car_maniability * delta
        car.apply_vector(car.direction_vector())

        if min(car.position) < 0:
            car.set_position(max(car.position[0], 0), max(car.position[1], 0))
        if max(car.position) > screen_width:
            car.set_position(min(car.position[0], screen_width), min(
                car.position[1], screen_width))
        if not car.detection(screen, SETTINGS.display_rays):
            running = False
            print("Votre voiture a touché un mur - fin de la partie")

        draw.general_stats(screen, fps_font, clock, None, None, start_time)
        pygame.display.flip()
        dt = clock.tick(fps)
    
    for _ in range(30):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        time.sleep(0.05)

def AI_loop(screen: pygame.Surface, circuit: dict, fps_font: pygame.font):
    print("Astuce : Appuyez sur la touche R si une voiture tourne en rond\n")
    clock = pygame.time.Clock()
    dt = 1
    init_pos, init_angle = calc_starting_pos(
        circuit["point1"], circuit["point2"])
    cars = [Car(circuit["bordures"], color= SETTINGS.colors["cars"], starting_pos=init_pos,
                abs_rotation=init_angle) for _ in range(SETTINGS.cars_number)]
    networks = [Network(c) for c in cars]
    running = True

    increment = 0

    def check_events() -> int:
        # 0 - continue
        # 1 - stop gen
        # 2 - stop everything
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 2
            if event.type == pygame.KEYDOWN:
                if event.unicode == "r":  # reset:
                    return 1
        return 0

    while running:
        increment += 1
        endgen = False
        start_time = time.time()
        while not endgen:

            temp = check_events()
            if temp == 1:
                endgen = True
                break
            elif temp == 2:
                # f.close()
                return

            screen.fill(SETTINGS.colors["background"])
            draw.circuit(screen, circuit["bordures"])
            draw.car(screen, (net.car for net in networks))

            # Gestion du mouvement de la voiture
            delta = dt * fps / 1000
            for net in networks:
                if net.dead == False:
                    net.update()
                    net.car.abs_rotation += SETTINGS.car_maniability * delta * net.direction

                    net.car.apply_vector(
                        net.car.direction_vector() * net.engine * 2)
                    if not net.car.detection(screen, SETTINGS.display_rays):
                        net.dead = True
                        net.car.death_time = time.time()

            survived = sum(1 for n in networks if not n.dead)
            if survived == 0:
                endgen = True

            draw.general_stats(screen, fps_font, clock,
                               increment, survived, start_time)
            draw.car_specs(screen, fps_font, networks[0])
            draw.car_network(screen, fps_font, networks[0])
            pygame.display.flip()
            dt = clock.tick(fps)

        arrival = circuit["bordures"][-1]  # ligne d'arrivée
        # calcul des scores
        for net in networks:
            net.score = net.car.get_score()
            if net.car.distance_to_segment(arrival.start, arrival.end) <= 8:
                net.score += 300  # points bonus si la voiture a atteint la ligne d'arrivée
        average = round(sum([net.score for net in networks])/len(networks))
        print(f"Génération N°{increment} terminée - score moyen : {average}")

        # Darwin
        networks = darwin(networks)

        # Reset des réseaux/voitures
        for net in networks:
            net.dead = 0
            # net.car.position = [80, 130]
            net.car.color = SETTINGS.colors["cars"]
            net.car.reset()
        networks[0].car.color = SETTINGS.colors["main_car"]


def main():
    print("""Lancement du programme

    Assurez-vous que toutes les dépendances utilisées soient installées sur votre ordinateur ;
    si besoin entrez `pip install -r requirements.txt` dans votre console
    """)

    # Chargement de la configuration
    global SETTINGS
    try:
        SETTINGS = load_from_filename("settings.yaml")
    except AssertionError as e:
        print("Erreur lors du chargement de la configuration :\n"+e.args[0])
        return

    draw.init()
    pygame.init()
    screen = pygame.display.set_mode(SETTINGS.screen_size)
    fps_font = pygame.font.SysFont('Arial', 18)
    pygame.display.set_caption("TIPE")
    border_colors = {
        "general": SETTINGS.colors["borders"],
        "begin": SETTINGS.colors["border-begin"],
        "end": SETTINGS.colors["border-end"]}
    circuit = circuit_creation(border_colors)

    if SETTINGS.manual_control:
        manual_loop(screen, circuit, fps_font)
    else:
        AI_loop(screen, circuit, fps_font)

    pygame.quit()


if __name__ == "__main__":
    main()
