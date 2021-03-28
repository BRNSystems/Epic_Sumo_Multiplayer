import pygame
import random
import math

from pygame.locals import *

pygame.init()


# dt it missing (the epic sumo is fps dependent)
class Spark:
    sparks = {}
    scroll = [0, 0]
    two_pi = round(math.pi * 2) * 100

    def __init__(self, pos, angle, speed, colorS, group, scale=1):
        self.object_pos = pos
        self.angle = angle
        self.speed = speed

        self.scale = scale
        self.scales = [self.scale * 3.5, self.scale * 0.3]

        self.color = colorS
        self.group = group

        # preparing math
        self.cosS = math.cos(self.angle) * self.speed
        self.L_cosS = math.cos(self.angle + math.pi / 2) * self.speed

        self.sinS = math.sin(self.angle) * self.speed
        self.L_sinS = math.sin(self.angle + math.pi / 2) * self.speed

    def move(self, display):
        self.object_pos[0] += self.cosS
        self.object_pos[1] += self.sinS

        self.draw(display)

        self.speed -= 0.2

        # im missing the other 2 funcs here didnt really needed them currently
        self.angle += 0.1

        if self.speed <= 0:
            self.delete_self(self)

        self.redo_math()

    def draw(self, display):
        scroll = self.get_scroll()

        c1 = self.L_cosS * self.scales[1]
        c2 = self.L_sinS * self.scales[1]

        p1 = [self.object_pos[0] + self.cosS * self.scale,
              self.object_pos[1] + self.sinS * self.scale]
        p2 = [self.object_pos[0] + c1,
              self.object_pos[1] + c2]
        p3 = [self.object_pos[0] - self.cosS * self.scales[0],
              self.object_pos[1] - self.sinS * self.scales[0]]
        p4 = [self.object_pos[0] - c1,
              self.object_pos[1] - c2]

        pygame.draw.polygon(display, self.color, [[p1[0] - scroll[0], p1[1] - scroll[1]],
                                                  [p2[0] - scroll[0], p2[1] - scroll[1]],
                                                  [p3[0] - scroll[0], p3[1] - scroll[1]],
                                                  [p4[0] - scroll[0], p4[1] - scroll[1]]])

    def redo_math(self):
        self.cosS = math.cos(self.angle) * self.speed
        self.L_cosS = math.cos(self.angle + math.pi / 2) * self.speed

        self.sinS = math.sin(self.angle) * self.speed
        self.L_sinS = math.sin(self.angle + math.pi / 2) * self.speed

    @classmethod
    def delete_self(cls, spark):
        cls.sparks[spark.group].remove(spark)

    @classmethod
    def central(cls, group, display):
        for spark in cls.sparks[group]:
            spark.move(display)

    # math.radians(random.randint(0, 360)),
    # random.uniform(0, cls.two_pi)
    @classmethod
    def generate(cls, group, pos, speed_lim, color_lim, scaler):
        cls.sparks[group].append(Spark(pos, random.randint(0, cls.two_pi) / 100,
                                       random.randint(speed_lim[0], speed_lim[1]),
                                       (random.randint(color_lim[0][0], color_lim[0][1]),
                                        random.randint(color_lim[1][0], color_lim[1][1]),
                                        random.randint(color_lim[2][0], color_lim[2][1])), group, scaler))

    @classmethod
    def create(cls, group, pos, speed_lim, color_lim, scaler, amount):
        for i in range(amount):
            cls.generate(group, pos.copy(), speed_lim, color_lim, scaler)

    @classmethod
    def create_3d(cls, group, pos, speed_lim, color_lim, scaler, amount):
        for i in range(amount):
            cls.generate(group, pos, speed_lim, color_lim, scaler)

    @classmethod
    def get_scroll(cls):
        return cls.scroll
