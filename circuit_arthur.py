import typing
import random
from math import hypot, sqrt
import math
import pygame
from pygame.math import Vector2 as Vector
from classes import Border

SCREEN_SIZE = (1200, 700)
START_POINT = (80, 100)
END_POINT = (1100, 600)
INTERMEDIATE_POINTS = [(160, 570), (515, 540), (565, 220), (900, 140)] # [(200, 500), (550, 610)]
MIN_ANGLE_DEGREES = 90 # 45
MAX_ANGLE_DEGREES = 175 # 45
MIN_SEGMENT_LENGTH = 40 # 100
MAX_COST_COEF = 1.0 # 1.8
RANDOM_GENPOINT_AMPLITUDE = 0.2 # 0.45
MIN_PATH_WIDTH = 70 # 70
MAX_PATH_WIDTH = 105 #100
GENERATIONS_NUMBER = 9 # 7


def calc_angle(point_a: tuple, point_b: tuple, point_c: tuple) -> float:
    "Calculate the angle ABC in degree"
    angle = math.degrees(math.atan2(point_c[1]-point_b[1], point_c[0]-point_b[0])
                         - math.atan2(point_a[1]-point_b[1], point_a[0]-point_b[0]))
    return angle-360 if angle > 180 else (360+angle if angle < -180 else angle)


def calc_distance(point_a: tuple, point_b: tuple) -> int:
    "Return the distance between A and B"
    return round(hypot(point_a[0]-point_b[0], point_a[1]-point_b[1]))


def generate_point(point_a: tuple, point_b: tuple, screen_size: tuple, last_move: tuple, i: int = 0) \
    -> ((int, int), (int, int)):
    "Generate a point between two other"
    i += 1
    cost = 1
    max_cost = 0
    angle = 0
    middle = [0, 0]
    middle[0] = (point_a[0]+point_b[0])//2
    middle[1] = (point_a[1]+point_b[1])//2
    min_angle = MIN_ANGLE_DEGREES
    # ---
    radius_max = max(abs(point_a[0] - point_b[0]), abs(point_a[1] - point_b[1]))
    last_move[0] = last_move[0] if random.random() < 0.7 else (1 if random.random() < 0.5 else -1)
    new_x = middle[0] + round(radius_max * random.uniform(0.001, RANDOM_GENPOINT_AMPLITUDE) * last_move[0])
    last_move[1] = last_move[1] if random.random() < 0.7 else (1 if random.random() < 0.5 else -1)
    new_y = middle[1] + round(radius_max * random.uniform(0.001, RANDOM_GENPOINT_AMPLITUDE) * last_move[1])
    # ---
    if i >= 700:
        return (new_x, new_y), last_move
    check_borders = MAX_PATH_WIDTH < new_x < screen_size[0]-MAX_PATH_WIDTH \
            and MAX_PATH_WIDTH < new_y < screen_size[1]-MAX_PATH_WIDTH
    if check_borders:
        distance_a_b = calc_distance(point_a, point_b)
        cost = round(distance_a_b
                     + calc_distance(point_b, (new_x, new_y))
                     - calc_distance(point_a, (new_x, new_y)))
        max_cost = round(distance_a_b * MAX_COST_COEF)
        if cost < max_cost:
            angle = abs(calc_angle(point_a, (new_x, new_y), point_b))
            min_angle += 250/sqrt(distance_a_b)
    print(cost, max_cost, "|", angle, min_angle, "|", i)
    if cost > max_cost or not check_borders or angle < MIN_ANGLE_DEGREES or angle > MAX_ANGLE_DEGREES:
        (new_x, new_y), last_move = generate_point(point_a, point_b, screen_size, last_move, i)
    return (round(new_x), round(new_y)), last_move

def check_angles(pathway: typing.List[tuple]) -> bool:
    """Check if there's any weird angle
    Return True if any point was deleted"""
    if len(pathway) < 3:
        return True
    result = True
    wrong_indexes = list()
    for index in range(1, len(pathway)-1):
        angle = abs(round(calc_angle(pathway[index-1], pathway[index], pathway[index+1])))
        if angle > 180:
            angle = 360-angle
        result = MIN_ANGLE_DEGREES < angle < MAX_ANGLE_DEGREES
        if not result:
            wrong_indexes.insert(0, index)
    for i in wrong_indexes:
        pathway.pop(i)
    if len(wrong_indexes) > 0:
        check_angles(pathway)
        return True
    return False


def add_width(pathway: typing.List[tuple], screen_size: tuple) -> typing.List[Border]:
    "Enlarge the pathway with a parallel border"
    points_over = list()
    points_under = list()
    result = list()
    delta = round(MIN_PATH_WIDTH/50), round(MIN_PATH_WIDTH/50)
    min_border = (screen_size[0]-MAX_PATH_WIDTH, screen_size[1]-MAX_PATH_WIDTH)
    for enum in range(len(pathway)-1):
        if enum > 0:
            angle = abs(calc_angle(pathway[enum-1], pathway[enum], pathway[enum+1]))
        else:
            angle = 170
        if angle < 150:
            points_over.append((pathway[enum][0], pathway[enum][1] - delta[0]))
            temp = min(pathway[enum][1]+MAX_PATH_WIDTH - delta[0], min_border[1])
            points_under.append((pathway[enum][0], temp))
        elif angle < 160:
            points_over.append((pathway[enum][0], pathway[enum][1] - delta[1]))
            temp = min(pathway[enum][1]+MIN_PATH_WIDTH - delta[1], min_border[1])
            points_under.append((pathway[enum][0], temp))
        else:
            points_over.append(pathway[enum])
            temp = min(pathway[enum][1]+MIN_PATH_WIDTH, min_border[1])
            points_under.append((pathway[enum][0], temp))
    for path in (points_over, points_under):
        for index in range(len(path)-1):
            color = ((index*100+70)%255, (index*90+20)%255, (index*50+40)%255)
            result.append(Border(path[index], path[index+1], color))
    return result

def add_width_2(pathway: typing.List[tuple]) -> typing.List[Border]:
    "Enlarge the pathway with a parallel border; version 2"
    points_over = list()
    points_under = list()
    result = list()
    delta = -round(MIN_PATH_WIDTH/12), round(MIN_PATH_WIDTH/12)
    # min_border = (screen_size[0]-MAX_PATH_WIDTH, screen_size[1]-MAX_PATH_WIDTH)
    new_delta = min(MIN_PATH_WIDTH + random.randrange(*delta), MAX_PATH_WIDTH)
    # First point
    vect = Vector(pathway[1][0]-pathway[0][0], pathway[1][1]-pathway[0][1])
    vect.rotate_ip(90)
    vect.scale_to_length(new_delta)
    points_over.append((pathway[0][0] - vect.x/2, pathway[0][1] - vect.y/2))
    points_under.append((pathway[0][0] + vect.x/2, pathway[0][1] + vect.y/2))
    print(new_delta)
    # Other points
    for enum in range(1, len(pathway)-1):
        point1, point2, point3 = pathway[enum-1], pathway[enum], pathway[enum+1]
        vect = Vector(point2[0]-point1[0], point2[1]-point1[1]) \
                + Vector(point3[0]-point2[0], point3[1]-point2[1])
        vect.rotate_ip(90)
        new_delta = max(min(new_delta + random.randrange(*delta), MAX_PATH_WIDTH), MIN_PATH_WIDTH)
        print(new_delta)
        vect.scale_to_length(new_delta)
        # points_over.append(point2)
        points_over.append((point2[0]-vect.x/2, point2[1]-vect.y/2))
        points_under.append((point2[0]+vect.x/2, point2[1]+vect.y/2))
    # Last point
    vect = Vector(pathway[-1][0]-pathway[-2][0], pathway[-1][1]-pathway[-2][1])
    vect.rotate_ip(90)
    vect.scale_to_length(new_delta)
    points_over.append((pathway[-1][0] - vect.x/2, pathway[-1][1] - vect.y/2))
    points_under.append((pathway[-1][0] + vect.x/2, pathway[-1][1] + vect.y/2))
    # Cleanup of points
    print(check_angles(points_over))
    print(check_angles(points_under))
    for path in (points_over, points_under):
        for index in range(len(path)-1):
            color = ((index*100+70)%255, (index*90+20)%255, (index*50+40)%255)
            if path[index][1] > SCREEN_SIZE[1]-10:
                path[index][1] = SCREEN_SIZE[1] - 10
            elif path[index][1] < 10:
                path[index][1] = 10
            result.append(Border(path[index], path[index+1], color))
    return result


def circuit_creation(*args):
    pathway = [START_POINT] + INTERMEDIATE_POINTS + [END_POINT]
    colors = [((index*100+70)%255, (index*90+20)%255, (index*50+40)%255) for index in range(120)]
    for _ in range(GENERATIONS_NUMBER):
        index2 = 0
        last_move = [-1, 1]
        for _ in range(len(pathway)-1):
            if calc_distance(pathway[index2], pathway[index2+1]) > MIN_SEGMENT_LENGTH:
                line = pathway[index2], pathway[index2+1]
                new_point, last_move = generate_point(*line, SCREEN_SIZE, last_move)
                pathway.insert(index2+1, new_point)
                index2 += 1
            index2 += 1
    print("\n", len(pathway), "points")
    return add_width_2(pathway)
