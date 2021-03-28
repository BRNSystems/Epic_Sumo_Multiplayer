import pygame
from pygame.locals import *

# basic config

pygame.mixer.pre_init(48000, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(16)


def get_sounds():
    sounds = {
        "click": pygame.mixer.Sound("assets/sounds/click.wav"),
        "collision": pygame.mixer.Sound("assets/sounds/collision.wav")
    }

    return sounds
