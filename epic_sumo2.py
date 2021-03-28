from s_engine import *
from spark import *
from ingame_funcs import *
import pygame
import sys
import time
import random
import math
from pygame.locals import *
import json
import threading
import asyncio
import websockets

# basic config
work = True

pygame.mixer.pre_init(48000, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(16)

font = pygame.font.SysFont('Comic Sans MS', 80)
small_font = pygame.font.SysFont('Comic Sans MS', 40)
tiny_font = pygame.font.SysFont('Comic Sans MS', 20)

players_defined = 0
connected = 0
global Player1
global Player2
uri = "ws://127.0.0.1:8765"
global websocket

async def write_players(arrx):
    global Player1
    global Player2
    Player1.all_ids = arrx[0]
    Player1.dir_movement = arrx[1]
    Player1.direction = arrx[2]
    Player1.ids_to_remove = arrx[3]
    Player1.memory = arrx[4]
    Player1.move.angle_speed = arrx[5]
    Player1.move.backwards = arrx[6]
    Player1.move.collisions = arrx[7]
    Player1.move.degree = arrx[8]
    Player1.move.force = arrx[9]
    Player1.move.forward = arrx[10]
    Player1.move.half_pi = arrx[11]
    Player1.move.left = arrx[12]
    Player1.move.offset = arrx[13]
    Player1.move.pi = arrx[14]
    Player1.move.right = arrx[15]
    Player1.move.speed = arrx[16]
    Player1.move.three_halves_pi = arrx[17]
    Player1.move.two_pi = arrx[18]
    Player1.move.vectors = arrx[19]
    Player1.movement = arrx[20]
    Player1.moving = arrx[21]
    Player1.object_id = arrx[22]
    Player1.object_pos = arrx[23]
    Player1.rect.bottom = arrx[24]
    Player1.rect.bottomleft = arrx[25]
    Player1.rect.bottomright = arrx[26]
    Player1.rect.center = arrx[27]
    Player1.rect.centerx = arrx[28]
    Player1.rect.centery = arrx[29]
    Player1.rect.h = arrx[30]
    Player1.rect.height = arrx[31]
    Player1.rect.left = arrx[32]
    Player1.rect.midbottom = arrx[33]
    Player1.rect.midleft = arrx[34]
    Player1.rect.midright = arrx[35]
    Player1.rect.midtop = arrx[36]
    Player1.rect.right = arrx[37]
    Player1.rect.size = arrx[38]
    Player1.rect.top = arrx[39]
    Player1.rect.topleft = arrx[40]
    Player1.rect.topright = arrx[41]
    Player1.rect.w = arrx[42]
    Player1.rect.width = arrx[43]
    Player1.rect.x = arrx[44]
    Player1.rect.y = arrx[45]
    Player1.size = arrx[46]
    Player1.special = arrx[47]
    Player1.specific.attribute = arrx[48]
    Player1.specific.attribute_0 = arrx[49]
    Player1.specific.attribute_1 = arrx[50]
    Player1.specific.attribute_2 = arrx[51]
    Player1.specific.boolean_attribute = arrx[52]
    Player1.specific.color_r = arrx[53]
    Player1.specific.fixed = arrx[54]
    Player1.specific.flip = arrx[55]
    Player1.specific.height = arrx[56]
    Player1.specific.object_id = arrx[57]
    Player1.specific.power = arrx[58]
    Player1.specific.scroll = arrx[59]
    Player1.specific.stage = arrx[60]
    Player1.type = arrx[61]

async def hello():
    global websocket
    global connected
    websocket = await websockets.connect(uri)
    connected = 1
    while True:
        greeting = await websocket.recv()
        try:
            if players_defined == 1:
                data = json.loads(greeting)[0]["data"]
                if len(data) == 62:
                    await write_players(data)
        except Exception as e:
            print(str(e))


loop = asyncio.get_event_loop()


def helloa():
    loop.run_until_complete(hello())
    loop.run_forever()


t = threading.Thread(target=helloa, args=tuple())
t.start()

while connected == 0:
    pass

Window_size = [900, 600]
screen = pygame.display.set_mode(Window_size)
display = pygame.Surface((1350, 900))
pygame.display.set_caption("Epic_sumo")
pygame.display.set_icon(pygame.image.load("assets/textures/icon.png").convert())
clock = pygame.time.Clock()


class Bg:
    active = []
    timer = 0

    bgs = {
        "first": pygame.image.load("assets/textures/backround/bg.png").convert(),
        "second": pygame.image.load("assets/textures/backround/bg-blue.png").convert()
    }
    bgs["first"].set_colorkey((255, 255, 255))
    bgs["second"].set_colorkey((255, 255, 255))

    def __init__(self, pos, speed, typeX):
        self.object_pos = pos
        self.speed = speed
        self.type = typeX

    @classmethod
    def generate(cls, amount, cord_lim=None):
        if cord_lim is None:
            cord_lim = [0, 1350]
        for i in range(amount):
            cls.active.append(Bg([random.randint(cord_lim[0], cord_lim[1]), random.randint(0, 860)],
                                 random.randint(2, 10), random.choice(("first", "second"))))

    @classmethod
    def blit_them(cls, display):
        for circle in cls.active:
            display.blit(cls.bgs[circle.type], circle.object_pos)

    @classmethod
    def remove_circle(cls, which):
        cls.active.remove(which)

    @classmethod
    def central(cls, display):
        for circle in cls.active:
            circle.move()

        cls.blit_them(display)

        if cls.timer == 0:
            cls.generate(12, [1350, 1500])
            cls.timer += 60
        else:
            cls.timer -= 1

    def move(self):
        self.object_pos[0] -= self.speed
        if self.object_pos[0] < -80:
            self.remove_circle(self)


class Solids:
    def __init__(self):
        self.stage = 0
        self.colors = [
            (73, 122, 67),
            (127, 182, 120),
            (181, 230, 29)
        ]

    def draw(self, solid, display, scroll):
        cc = (self.stage // 40) % 3
        current_stage = self.stage % 40
        mid_point = [
            solid.object_pos[0] + (solid.size[0] / 2),
            solid.object_pos[1] + (solid.size[1] / 2)
        ]

        pygame.draw.rect(display, self.colors[cc], pygame.Rect(mid_point[0] - current_stage - scroll.scroll[0],
                                                               mid_point[1] - current_stage - scroll.scroll[1],
                                                               current_stage * 2, current_stage * 2))

    def draw_solids(self, objects, display, scroll):
        for obj in objects.game_objects:
            if obj.type == "solid":
                self.draw(obj, display, scroll)
        self.stage += 1


def menu(screenX, fs):
    def mouse_check(mouse_pos, menu_flow):

        new_list = [0, 0, menu_flow[2], menu_flow[3], 0, 0]

        # settings
        if 800 < mouse_pos[0] < 872:
            if 500 < mouse_pos[1] < 572:
                new_list[0] = 1

        # play
        if 300 < mouse_pos[0] < 591:
            if 300 < mouse_pos[1] < 396:
                new_list[1] = 1

        # change player 1
        if 250 < mouse_pos[0] < 359:
            if 500 < mouse_pos[1] < 548:
                new_list[4] = 1

        # change player 2
        if 400 < mouse_pos[0] < 509:
            if 500 < mouse_pos[1] < 548:
                new_list[5] = 1

        return new_list

    # preparations

    game = Game()
    game.game_flow["menu"] = [0, 0, 0, 0, 0, 0]
    game.game_flow["sounds"] = get_sounds()
    settings_on_top = False
    display = pygame.Surface((900, 600))

    abilities = {
        "1.player": "dash",
        "2.player": "dash",
        "1.storage": 5,
        "2.storage": 5
    }

    menu_textures = {
        "bg": pygame.image.load("assets/textures/menu/main_menu.png").convert(),
        "play": pygame.image.load("assets/textures/menu/play_button.png").convert(),
        "play_pressed": pygame.image.load("assets/textures/menu/play_button_pressed.png").convert(),
        "settings": pygame.image.load("assets/textures/menu/settings_btn.png").convert(),
        "settings_pressed": pygame.image.load("assets/textures/menu/settings_btn_pressed.png").convert(),
        "change": pygame.image.load("assets/textures/menu/change_btn.png").convert(),
        "change_pressed": pygame.image.load("assets/textures/menu/change_btn_pressed.png").convert(),
        "dash": pygame.image.load("assets/textures/menu/dash.png").convert(),
        "shockwave": pygame.image.load("assets/textures/menu/wave.png").convert(),
        "ice": pygame.image.load("assets/textures/menu/ice.png").convert(),
        "settings_menu": pygame.image.load("assets/textures/menu/settings.png").convert()
    }

    # game loop
    while game.alive:
        display.blit(menu_textures["bg"], [0, 0])

        # event loop

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                game.game_flow["menu"] = mouse_check(mousepos, game.game_flow["menu"])

                # setting actions for buttons
                if settings_on_top is False:
                    if game.game_flow["menu"][1]:
                        game.game_flow["sounds"]["click"].play(0)
                        arena(screenX, fs, abilities)

                    elif game.game_flow["menu"][4]:
                        game.game_flow["menu"][2] += 1
                        if game.game_flow["menu"][2] > 2:
                            game.game_flow["menu"][2] = 0

                        game.game_flow["sounds"]["click"].play(0)

                    elif game.game_flow["menu"][5]:
                        game.game_flow["menu"][3] += 1
                        if game.game_flow["menu"][3] > 2:
                            game.game_flow["menu"][3] = 0

                        game.game_flow["sounds"]["click"].play(0)

                # settings menu

                if game.game_flow["menu"][0]:
                    settings_on_top = not settings_on_top
                    game.game_flow["sounds"]["click"].play(0)

            if event.type == pygame.MOUSEMOTION:
                # if mouse moving get mouse pos
                mousepos = pygame.mouse.get_pos()
                # function that checks if mouse is above any button and changes image, color of that image
                game.game_flow["menu"] = mouse_check(mousepos, game.game_flow["menu"])

            if event.type == KEYDOWN:
                if event.key == K_f:
                    fs = not fs
                    if fs is False:
                        screenX = pygame.display.set_mode(Window_size)
                    else:
                        screenX = pygame.display.set_mode(Window_size, pygame.FULLSCREEN)

                elif event.key == K_ESCAPE:
                    if settings_on_top is False:
                        pygame.quit()
                        sys.exit()
                    else:
                        settings_on_top = not settings_on_top

        # making menu

        if game.game_flow["menu"][1]:
            display.blit(menu_textures["play_pressed"], [300, 300])
        else:
            display.blit(menu_textures["play"], [300, 300])

        # showing ability of 1.player
        if game.game_flow["menu"][2] == 0:
            display.blit(menu_textures["dash"], [100, 400])
            abilities["1.player"] = "dash"
            abilities["1.storage"] = 10
        elif game.game_flow["menu"][2] == 1:
            display.blit(menu_textures["shockwave"], [100, 400])
            abilities["1.player"] = "wave"
            abilities["1.storage"] = 8
        elif game.game_flow["menu"][2] == 2:
            display.blit(menu_textures["ice"], [100, 400])
            abilities["1.player"] = "ice"
            abilities["1.storage"] = 10

        # showing ability of 2.player
        if game.game_flow["menu"][3] == 0:
            display.blit(menu_textures["dash"], [500, 400])
            abilities["2.player"] = "dash"
            abilities["2.storage"] = 10
        elif game.game_flow["menu"][3] == 1:
            display.blit(menu_textures["shockwave"], [500, 400])
            abilities["2.player"] = "wave"
            abilities["2.storage"] = 8
        elif game.game_flow["menu"][3] == 2:
            display.blit(menu_textures["ice"], [500, 400])
            abilities["2.player"] = "ice"
            abilities["2.storage"] = 10

        if game.game_flow["menu"][4] == 0:
            display.blit(menu_textures["change"], [250, 500])
        elif game.game_flow["menu"][4] == 1:
            display.blit(menu_textures["change_pressed"], [250, 500])

        if game.game_flow["menu"][5] == 0:
            display.blit(menu_textures["change"], [400, 500])
        elif game.game_flow["menu"][5] == 1:
            display.blit(menu_textures["change_pressed"], [400, 500])

        if settings_on_top:
            display.blit(menu_textures["settings_menu"], [0, 0])

        if game.game_flow["menu"][0]:
            display.blit(menu_textures["settings_pressed"], [800, 500])
        else:
            display.blit(menu_textures["settings"], [800, 500])

        # basic loop config

        screenX.blit(display, (0, 0))
        pygame.display.update()
        clock.tick(60)


def arena(screenX, fs, abilities):
    global Player1
    global Player2
    global players_defined
    ids = Id()
    images_dictionary = {"solid": pygame.image.load("assets/textures/game/solid.png").convert(),
                         "circle": pygame.image.load("assets/textures/backround/circle_arena.png").convert()}
    images_dictionary["circle"].set_colorkey((0, 0, 0))
    images_dictionary["solid"].set_colorkey((0, 0, 0))
    game = Game()
    game.game_flow["collision_timer"] = 0
    game.game_flow["boost"] = 0.9
    game.game_flow["speed_timer"] = 0
    game.game_flow["winner"] = "na"
    game.game_flow["inputs"] = True
    game.game_flow["sounds"] = get_sounds()

    new_parameters = [1350, 900]
    display = pygame.Surface((1350, 900))

    # background

    bg = Bg
    bg.generate(100)

    # solids

    solids = Solids()

    # loading map

    mapX = load_map("assets/maps/map0")

    # loading objects

    objects = Objects()

    # loading bg circle

    midpoint = [816, 672]
    circle = Object("circle", game.custom_id_giver, [192, 0], [0, 0], 0, False, [1248, 1344])
    sort(circle, objects)
    game.custom_id_giver += 1

    # loading from map

    load_objects(mapX, 96, 96, objects, game)

    # players

    # never set direction to 0
    Player1 = Object("player", game.custom_id_giver, [800, 800], [0, 0],
                     round(math.tau * 0.75, 2), True, [10, 10], True)
    Player1.specific.images.append(pygame.image.load("assets/textures/game/player.png").convert())
    Player1.specific.images[0].set_colorkey((0, 0, 0))
    Player1.move.collisions = True  # enables collisions for player
    Player1.move.speed = 0.5  # increasing speed so ur not super slow
    Player1.move.angle_speed = 0.1

    # simulating movement so u dont start at speed 0
    Player1.dir_movement = Player1.move.set_start_dir_movement(Player1.direction, Player1.dir_movement)

    # sorts player
    sort(Player1, objects)
    # moves to next id
    game.custom_id_giver += 1

    # player 2

    # never set direction to 0
    Player2 = Object("player", game.custom_id_giver, [800, 400], [0, 0], round(math.pi/2, 2), True, [10, 10], True)
    Player2.specific.images.append(pygame.image.load("assets/textures/game/player.png").convert())
    Player2.specific.images[0].set_colorkey((0, 0, 0))
    Player2.move.collisions = True  # enables collisions for player
    Player2.move.speed = 0.5  # increasing speed so ur not super slow
    Player2.move.angle_speed = 0.1

    # simulating movement so u dont start at speed 0
    Player2.dir_movement = Player2.move.set_start_dir_movement(Player2.direction, Player2.dir_movement)

    # sorts player
    sort(Player2, objects)
    # moves to next id
    game.custom_id_giver += 1
    players_defined = 1
    # sparks

    sparks = Spark
    sparks.sparks["a"] = []
    sparks.sparks["b"] = []
    pointers = [pygame.image.load("assets/textures/game/p1_pointer.png").convert(),
                pygame.image.load("assets/textures/game/p2_pointer.png").convert()]
    for point in pointers:
        point.set_colorkey((0, 0, 0))

    # scroll

    scroll = Scroll([0, 0])

    # ending

    winner_text = pygame.image.load("assets/textures/menu/template_for_text.png").convert()
    esc = pygame.image.load("assets/textures/menu/esc.png").convert()

    # game loop

    while game.alive:
        # checking if end

        check_loser(midpoint, [Player1, Player2], game)

        # setting up bg

        display.fill((20, 20, 20))
        bg.central(display)

        # checking for removed objects

        objects.destroy_trash(ids)

        ids.remove_by_id(objects)

        # doing player movement

        Player1.movement = Player1.move.move(Player1.dir_movement)
        Player1.direction, Player1.dir_movement = Player1.move.change_dir(Player1.direction,
                                                                          Player1.move.angle_speed)
        Player2.movement = Player2.move.move(Player2.dir_movement)
        Player2.direction, Player2.dir_movement = Player2.move.change_dir(Player2.direction,
                                                                          Player2.move.angle_speed)

        # second parameter is speed of rotation

        # collisions

        objects.do_collisions(objects)

        players_collisions(Player1, Player2, game)

        # new sparks
        sparks.scroll = scroll.scroll

        sparks.create("a", Player1.object_pos, [3, 5], [[10, 255], [0, 200], [0, 0]], 3, 1)
        sparks.create("b", Player2.object_pos, [3, 5], [[0, 0], [0, 200], [10, 255]], 3, 1)

        # sounds

        # displaying objects

        scroll.move_scroll(Player1, [900, 600], "both", 30)
        scroll.move_scroll(Player2, [900, 600], "both", 30)

        load_textures(objects, images_dictionary, display, scroll)

        solids.draw_solids(objects, display, scroll)

        display_pointers(display, [Player1, Player2], pointers, scroll)

        sparks.central("a", display)
        sparks.central("b", display)

        # event loop

        if game.game_flow["inputs"]:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_f:
                        fs = not fs
                        if fs is False:
                            screenX = pygame.display.set_mode(Window_size)
                        else:
                            screenX = pygame.display.set_mode(new_parameters, pygame.FULLSCREEN)

                    elif event.key == K_ESCAPE:
                        game.game_flow["sounds"]["click"].play(0)
                        game.alive = False

                    elif event.key == K_d:
                        Player2.move.right = True
                    elif event.key == K_a:
                        Player2.move.left = True
                    elif event.key == K_w:
                        Player2.move.forward = True
                    elif event.key == K_e:
                        if abilities["2.storage"] > 0:
                            if abilities["2.player"] == "ice":
                                Player2.move.vectors = []
                            elif abilities["2.player"] == "dash":
                                Player2.move.vectors.append([Player2.dir_movement[0] * game.game_flow["boost"],
                                                             Player2.dir_movement[1] * game.game_flow["boost"]])
                            elif abilities["2.player"] == "wave":
                                Player1.move.vectors.append(
                                    get_shockwave_vector(Player2.object_pos, Player1.object_pos))
                            abilities["2.storage"] -= 1

                # key_up

                elif event.type == KEYUP:

                    if event.key == K_d:
                        Player2.move.right = False
                    elif event.key == K_a:
                        Player2.move.left = False
                    elif event.key == K_w:
                        Player2.move.forward = False

        else:
            stop_inputs([Player1, Player2])
            winner = font.render(f"Winner is : {game.game_flow['winner']}",
                                 False, (255, 255, 255))
            display.blit(winner_text, [50, 50])
            display.blit(winner, [90, 80])
            display.blit(esc, [500, 450])

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_f:
                        fs = not fs
                        if fs is False:
                            screenX = pygame.display.set_mode(Window_size)
                        else:
                            screenX = pygame.display.set_mode(new_parameters, pygame.FULLSCREEN)

                    elif event.key == K_ESCAPE:
                        game.game_flow["sounds"]["click"].play(0)
                        game.alive = False

        # basic loop config

        outarr = [Player2.all_ids, Player2.dir_movement, Player2.direction, Player2.ids_to_remove, Player2.memory, Player2.move.angle_speed, Player2.move.backwards, Player2.move.collisions, Player2.move.degree, Player2.move.force, Player2.move.forward, Player2.move.half_pi, Player2.move.left, Player2.move.offset, Player2.move.pi, Player2.move.right, Player2.move.speed, Player2.move.three_halves_pi, Player2.move.two_pi, Player2.move.vectors, Player2.movement, Player2.moving, Player2.object_id, Player2.object_pos, Player2.rect.bottom, Player2.rect.bottomleft, Player2.rect.bottomright, Player2.rect.center, Player2.rect.centerx, Player2.rect.centery, Player2.rect.h, Player2.rect.height, Player2.rect.left, Player2.rect.midbottom, Player2.rect.midleft, Player2.rect.midright, Player2.rect.midtop, Player2.rect.right, Player2.rect.size, Player2.rect.top, Player2.rect.topleft, Player2.rect.topright, Player2.rect.w, Player2.rect.width, Player2.rect.x, Player2.rect.y, Player2.size, Player2.special, Player2.specific.attribute, Player2.specific.attribute_0, Player2.specific.attribute_1, Player2.specific.attribute_2, Player2.specific.boolean_attribute, Player2.specific.color_r, Player2.specific.fixed, Player2.specific.flip, Player2.specific.height, Player2.specific.object_id, Player2.specific.power, Player2.specific.scroll, Player2.specific.stage, Player2.type]
        datasend = json.dumps({"player": 2, "data": outarr})
        asyncio.run(websocket.send(datasend))
        screenX.blit(pygame.transform.scale(display, new_parameters), (0, 0))
        pygame.display.update()
        clock.tick(60)


menu(screen, False)
