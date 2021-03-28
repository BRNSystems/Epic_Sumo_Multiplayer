import pygame
import sys
import time
import random
import math
import copy
from pygame.locals import *

pygame.init()


# has attributes for basic thing in game
class Game:
    def __init__(self, game_maps=None):
        self.alive = True
        # fs = fullscreen
        self.fs = False
        self.custom_id_giver = 0

        self.game_flow = {}

        self.game_maps = None
        # checks if there are any maps if there are puts them in self.game_maps
        if game_maps is not None:
            self.game_maps = game_maps


# stores objects in a sorted way
class Objects:
    def __init__(self):
        self.game_objects = []
        self.collision_objects = []
        self.moving_objects = []

        # dunno if next att will be useful
        # u add ids of objects u want to delete there is no func to delete for now

        self.objects_to_delete = []

        self.values = {
            "pos_to_del": []
        }

    def do_collisions(self, objects):
        for obj in self.collision_objects:
            collision(obj, objects)

    def destroy_trash(self, ids):
        for trash in self.objects_to_delete:
            ids.ids_to_remove.append(trash)
        self.objects_to_delete = []

    def take_out_trash(self, ids):
        for obj in self.objects_to_delete:
            ids.ids_to_remove.append(obj)
        self.objects_to_delete = []


# Id class just stores all ids of all objects
class Id:
    all_ids = []
    ids_to_remove = []

    def remove_by_id(self, objects):
        for item in self.ids_to_remove:
            for obj in objects.game_objects:
                if obj.object_id == item:
                    g_index = objects.game_objects.index(obj)
                    if obj.moving:
                        m_index = objects.moving_objects.index(obj)
                        if obj.move.collisions:
                            c_index = objects.collision_objects.index(obj)

                            del objects.collision_objects[c_index]

                        del objects.moving_objects[m_index]

                    del objects.game_objects[g_index]

        self.ids_to_remove = []


class Scroll:
    def __init__(self, scroll):
        self.scroll = scroll
        self.fade = 20
        self.safe_fade = 20
        self.in_progress = False
        self.save_scroll = self.scroll

    def move_scroll(self, player, screen, which, space=20):
        if which == "y" or which == "both":
            self.scroll[1] += (player.rect.y - self.scroll[1] - (screen[1] / 2) + (player.size[1] / 2)) / space
            self.scroll[1] = int(self.scroll[1])
        if which == "x" or which == "both":
            self.scroll[0] += (player.rect.x - self.scroll[0] - (screen[0] / 2) + (player.size[0] / 2)) / space
            self.scroll[0] = int(self.scroll[0])

    def add_scroll(self, which, how_much, fade=None):
        if fade is not None:
            self.safe_fade = fade
            if self.in_progress is False:
                self.load_safe_fade()
                self.save_scroll = self.scroll
                self.in_progress = True
            how_much[0] /= self.fade
            how_much[1] /= self.fade
            self.fade += 0.01 * self.fade

        if which == "x" or which == "both":
            self.scroll[0] += how_much[0]
            self.scroll[0] = round(self.scroll[0])

        if which == "y" or which == "both":
            self.scroll[1] += how_much[1]
            self.scroll[1] = round(self.scroll[1])

    def load_safe_fade(self):
        self.fade = self.safe_fade
        self.in_progress = False


class Special:
    def __init__(self, object_id):
        self.object_id = object_id
        self.stage = ""
        self.attribute = ""
        self.images = []
        self.attribute_0 = 0
        self.attribute_1 = 0
        self.attribute_2 = 0
        self.color_r = [0, 0, 0]
        self.boolean_attribute = False
        self.height = 0
        self.power = 0
        self.flip = False
        self.scroll = False
        self.fixed = False


# collisions class take care of collision funcs
# !!!!!!!!!! holds init for Object !!!!!!!!!!!!!!!!!!!
# class purely for inheritance
class Collisions(Id):

    def __init__(self, typeX, object_id, x_y, movement, direction, moving, size, special=None):
        self.type = typeX
        self.object_id = object_id
        self.object_pos = x_y
        self.movement = movement
        self.direction = direction
        self.moving = moving
        self.size = size
        self.dir_movement = [0.0, 0.0]
        self.memory = []
        self.special = special
        if self.object_id != self.all_ids:
            self.all_ids.append(self.object_id)
        else:
            print("duplicate/ linked object")

        # giving it bonus classes

        if self.moving:
            self.move = Moving_Object()
        if self.special:
            self.specific = Special(self.object_id)

        self.rect = pygame.Rect(self.object_pos[0], self.object_pos[1], self.size[0], self.size[1])

    # theres a function for every type of collisions
    # edit collisions here (I added some basic ones just so u can see)
    # self if objects that it hit and obj is the object that hit smt

    # always add both side of collisions (ask who collided with whom)

    def hit_bottom(self, obj, objects):
        if self.type == "solid":
            if obj.type == "player":
                obj.rect.bottom = self.rect.top
                obj.object_pos = [obj.rect.x, obj.rect.y]
                self.memory[0] -= 1
                if self.memory[0] == 0:
                    objects.objects_to_delete.append(self.object_id)

                opposite = obj.move.get_final_vector()
                opp = [-opposite[0] * 0.4, -opposite[1] * 0.8]
                obj.move.vectors.append(opp)

    def hit_top(self, obj, objects):
        if self.type == "solid":
            if obj.type == "player":
                obj.rect.top = self.rect.bottom
                obj.object_pos = [obj.rect.x, obj.rect.y]
                self.memory[0] -= 1
                if self.memory[0] == 0:
                    objects.objects_to_delete.append(self.object_id)

                opposite = obj.move.get_final_vector()
                opp = [-opposite[0] * 0.4, -opposite[1] * 0.8]
                obj.move.vectors.append(opp)

    def hit_left(self, obj, objects):
        if self.type == "solid":
            if obj.type == "player":
                obj.rect.left = self.rect.right
                obj.object_pos = [obj.rect.x, obj.rect.y]
                self.memory[0] -= 1
                if self.memory[0] == 0:
                    objects.objects_to_delete.append(self.object_id)

                opposite = obj.move.get_final_vector()
                opp = [-opposite[0] * 0.4, -opposite[1] * 0.8]
                obj.move.vectors.append(opp)

    def hit_right(self, obj, objects):
        if self.type == "solid":
            if obj.type == "player":
                obj.rect.right = self.rect.left
                obj.object_pos = [obj.rect.x, obj.rect.y]
                self.memory[0] -= 1
                if self.memory[0] == 0:
                    objects.objects_to_delete.append(self.object_id)

                opposite = obj.move.get_final_vector()
                opp = [-opposite[0] * 0.4, -opposite[1] * 0.8]
                obj.move.vectors.append(opp)


# next 2 classes are for object class
class Moving_Object:
    def __init__(self):
        # consts
        self.degree = 0.0174533
        self.pi = math.pi
        self.half_pi = round(math.pi / 2, 6)
        self.two_pi = round(math.pi * 2, 6)
        self.three_halves_pi = round(3 * (math.pi / 2), 6)
        self.speed = 1
        self.force = 3
        self.offset = 0
        self.vectors = []

        self.forward = False
        self.backwards = False
        self.left = False
        self.right = False

        self.collisions = False

    def move(self, dir_movement):

        movement = dir_movement

        return movement

    # dir is the angle the player is facing
    def change_dir(self, direction, angle):

        new_vector = [0, 0]

        if self.left:
            direction -= angle
            if direction < 0:
                direction += self.two_pi
            new_vector[0] = round(math.cos(direction) * self.speed, 2)
            new_vector[1] = round(math.sin(direction) * self.speed, 2)
            self.vectors.append(new_vector)
        elif self.right:
            direction += angle
            if direction > self.two_pi:
                direction -= self.two_pi
            new_vector[0] = round(math.cos(direction) * self.speed, 2)
            new_vector[1] = round(math.sin(direction) * self.speed, 2)
            self.vectors.append(new_vector)
        elif self.forward:
            new_vector[0] = round(math.cos(direction) * self.speed, 2)
            new_vector[1] = round(math.sin(direction) * self.speed, 2)
            self.vectors.append(new_vector)

        return direction, self.get_final_vector()

    # used for setting things before game loop
    def set_start_dir_movement(self, direction, dir_movement):
        dir_movement[0] = round(math.cos(direction + (self.offset * self.degree)) * self.speed, 2)
        dir_movement[1] = round(math.sin(direction + (self.offset * self.degree)) * self.speed, 2)
        return dir_movement

    def get_final_vector(self):
        to_remove = []
        for i in range(len(self.vectors)-1):
            self.vectors[i][0] *= 0.96
            self.vectors[i][1] *= 0.96
            if abs(self.vectors[i][0]) < 0.2 and abs(self.vectors[i][1]) < 0.2:
                to_remove.append(self.vectors[i])

        for item in to_remove:
            self.vectors.remove(item)

        final_vector = [0, 0]

        for vector in self.vectors:
            final_vector[0] += vector[0]
            final_vector[1] += vector[1]

        return final_vector


class Object(Collisions):
    def __init__(self, typeX, object_id, x_y, movement, direction, moving, size, special=None):
        super().__init__(typeX, object_id, x_y, movement, direction, moving, size, special)

    def __str__(self):
        return self.type

    # changes position along with the rect
    def change_pos(self, x_y):
        self.object_pos = x_y
        self.rect = pygame.Rect(self.object_pos[0], self.object_pos[1], self.size[0], self.size[1])


def distance_indicator(coords1, coords2):
    x_distance = abs(coords1[0] - coords2[0])
    y_distance = abs(coords1[1] - coords2[1])
    distance = math.sqrt((x_distance ** 2) + (y_distance ** 2))
    return round(distance, 4)


def load_images(path, name, number_of_images, file_type=".png"):
    images = []
    for i in range(number_of_images):
        images.append(pygame.image.load("{}/{}{}{}".format(path, name, i, file_type)).convert())
    return images


def load_map(path):
    f = open(path, "r")
    data = f.read()
    f.close()
    data = data.split('\n')
    product = []
    for line in data:
        product.append(list(line))
    return product


# next func sorts object into objects class so the objects is stored where it should be
def sort(obj, objects):
    objects.game_objects.append(obj)

    if obj.moving:
        objects.moving_objects.append(obj)

        if obj.move.collisions:
            objects.collision_objects.append(obj)


def find_collisions(obj, objects):
    hit_list = []
    for element in objects.game_objects:
        if element.object_id != obj.object_id:
            if element.rect.colliderect(obj.rect):
                hit_list.append(element)
    return hit_list


def collision(obj, objects):
    # collisions for left/right
    obj.change_pos([obj.object_pos[0] + obj.movement[0], obj.object_pos[1]])
    hit_list = find_collisions(obj, objects)
    for item in hit_list:
        if obj.movement[0] > 0:
            item.hit_right(obj, objects)
        elif obj.movement[0] < 0:
            item.hit_left(obj, objects)

    # collisions for top/bottom
    obj.change_pos([obj.object_pos[0], obj.object_pos[1] + obj.movement[1]])
    hit_list = find_collisions(obj, objects)
    for item in hit_list:
        if obj.movement[1] > 0:
            item.hit_bottom(obj, objects)
        elif obj.movement[1] < 0:
            item.hit_top(obj, objects)


# !!!!!!!!!!! config this function for every program !!!!!!!!!!
def load_objects(game_map, width, height, objects, game):
    x, y = 0, 0
    for line in game_map:
        for obj in line:
            # this is just to be efficient normaly u can use elif and put another obj to another num
            if obj == "1":
                obj = Object("solid", game.custom_id_giver, [x, y], [0, 0], 0, False, [width, height])
                obj.memory.append(3)
                sort(obj, objects)
                game.custom_id_giver += 1
            x += width
        y += height
        x = 0


def load_textures(objects, dictionary, display, scroll):
    for object in objects.game_objects:
        if object.special:
            display.blit(object.specific.images[object.specific.attribute_0],
                         [object.object_pos[0] - scroll.scroll[0], object.object_pos[1] - scroll.scroll[1]])
        else:
            display.blit(dictionary["{}".format(object.type)],
                         [object.object_pos[0] - scroll.scroll[0], object.object_pos[1] - scroll.scroll[1]])


def load_sp_texture(objects, type_x, image):
    for object in objects.special_objects:
        if object.type == type_x:
            object.attributes.images.append(image)


def load_bg(image, y_x, width, height, display):
    pos = [0, 0]
    for i in range(y_x[0]):
        for j in range(y_x[1]):
            display.blit(image, pos)
            pos[0] += width
        pos[0] = 0
        pos[1] += height


def find_angle_between_points(center, point):
    dists = distances(center, point)
    try:
        angle = math.atan(dists[1] / dists[0])

        if point[0] < center[0]:
            if point[1] < center[1]:
                return angle + math.pi
            else:
                return (math.pi / 2 - angle) + (math.pi / 2)
        else:
            if point[1] < center[1]:
                return (math.pi / 2 - angle) + 3 * (math.pi / 2)
            else:
                return angle
    except ZeroDivisionError:
        return False


def distances(cords1, cords2):
    return [abs(cords1[0] - cords2[0]), abs(cords1[1] - cords2[1])]


def average(*args):
    sumX = 0
    for item in args:
        sumX += item
    return sumX/len(args)


def area_intersection_of_circles(points, radius_list):
    try:
        dist = distance_indicator(points[0], points[1])

        alpha_cos = (pow(radius_list[1], 2) + pow(dist, 2) - pow(radius_list[0], 2)) / (2 * radius_list[1] * dist)

        alpha = math.acos(alpha_cos)

        beta_cos = (dist - alpha_cos * radius_list[1]) / radius_list[0]

        beta = math.acos(beta_cos)

        triangles = (alpha_cos * pow(radius_list[1], 2) * math.sin(alpha)) + (
                    beta_cos * pow(radius_list[0], 2) * math.sin(beta))

        arcs = ((math.pi * pow(radius_list[0], 2) * beta * 2) / math.tau) + (
                    (math.pi * pow(radius_list[1], 2) * alpha * 2) / math.tau)

        return arcs - triangles
    except:
        return False
