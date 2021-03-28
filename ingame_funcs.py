import math
from s_engine import *
import pygame
from pygame.locals import *
from Sounds import get_sounds

# basic config

pygame.mixer.pre_init(48000, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(16)


def between_player_collisions(player1, player2, game):
    if game.game_flow["collision_timer"] == 0:

        dist = distance_indicator(player1.object_pos, player2.object_pos)

        if dist < 75:
            game.game_flow["sounds"]["collision"].play(0)

            player1.move.vectors.append([player2.dir_movement[0] * player2.move.force,
                                         player2.dir_movement[1] * player2.move.force])
            player2.move.vectors.append([player1.dir_movement[0] * player1.move.force,
                                         player1.dir_movement[1] * player1.move.force])
            game.game_flow["collision_timer"] += 20
    else:
        game.game_flow["collision_timer"] -= 1


def players_collisions(player1, player2, game):
    if game.game_flow["collision_timer"] == 0:

        dist = distance_indicator(player1.object_pos, player2.object_pos)

        if dist < 75:
            game.game_flow["sounds"]["collision"].play(0)

            ag1 = find_angle_between_points(player1.object_pos, player2.object_pos)
            ag2 = ag1 + math.pi

            forces = [average(abs(player1.dir_movement[0]), abs(player1.dir_movement[1])) * player1.move.force,
                      average(abs(player2.dir_movement[0]), abs(player2.dir_movement[1])) * player2.move.force]

            player1.move.vectors.append([math.cos(ag2) * forces[1],
                                         math.sin(ag2) * forces[1]])
            player2.move.vectors.append([math.cos(ag1) * forces[0],
                                         math.sin(ag1) * forces[0]])
            game.game_flow["collision_timer"] += 20
    else:
        game.game_flow["collision_timer"] -= 1


def get_shockwave_vector(pos1, pos2, divider=14):
    dist = (100 / (distance_indicator(pos1, pos2) + 0.0001))

    x_wave = (-(pos1[0] - pos2[0]) / divider) * dist
    y_wave = (-(pos1[1] - pos2[1]) / divider) * dist

    # divider is there to make the shockwave less powerfull

    return [x_wave, y_wave]


def check_loser(midpoint, players, game):
    dists = [
        distance_indicator(midpoint, players[0].object_pos),
        distance_indicator(midpoint, players[1].object_pos)
    ]
    for i in range(2):
        if dists[i] > 680:
            if game.game_flow["inputs"] is False:
                game.game_flow["winner"] = "draw"
            game.game_flow["inputs"] = False
            if i == 0:
                game.game_flow["winner"] = "p2"
            else:
                game.game_flow["winner"] = "p1"


def stop_inputs(players):
    for player in players:
        player.move.forward = False
        player.move.left = False
        player.move.right = False


def display_pointers(display, players, pointers, scroll):
    index = 0
    for player in players:
        angle = find_angle_between_points(player.object_pos, [player.object_pos[0] + math.cos(player.direction),
                                                              player.object_pos[1] + math.sin(player.direction)])
        if angle is False:
            index += 1
            continue

        display.blit(pygame.transform.rotate(pointers[index], math.degrees(-angle)),
                     [(player.object_pos[0] + math.cos(angle) * 40) - scroll.scroll[0] - 12,
                      (player.object_pos[1] + math.sin(angle) * 40) - scroll.scroll[1] - 12])
        index += 1