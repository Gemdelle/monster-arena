import pygame
from sys import exit  # to exit the game without having issues with the True loop
from random import randint
import math

from Config.config import config


# 01. Basic Setup
# 02. Surfaces

def displayScore():
    current_time = (int(pygame.time.get_ticks() / 1000) - start_time) 
    score_surf = test_font.render(str(current_time),False,'White')
    score_rect = score_surf.get_rect(center = (945,103))
    screen.blit(score_surf,score_rect)

    return current_time


def bad_atom_movement(obstacle_list):
    global bad_atom_spawn_count

    if obstacle_list:
        for obstacle_rec in obstacle_list:
            obstacle_rec.x -= 5

            screen.blit(bad_atom_surf,obstacle_rec)

        obstacle_list = [obstacle for obstacle in obstacle_list if
                         obstacle.x > -200]  # delete snails that are beyond -100(x)

        return obstacle_list
    else:
        return []


def good_atom_movement(obstacle_list):
    global good_atom_spawn_count

    if obstacle_list:
        for obstacle_rec in obstacle_list:
            obstacle_rec.x -= 5

            # if obstacle_rec.bottom <= 1000:
            screen.blit(good_atom_surf,obstacle_rec)

        obstacle_list = [obstacle for obstacle in obstacle_list if
                         obstacle.x > -200]  # delete snails that are beyond -100(x)

        return obstacle_list
    else:
        return []

def collisions(player,objects):
    if objects:
        for object_rect in objects:
            if player.colliderect(object_rect):
                return False
    return True

# def atomsCollisions(player,objects):
#     if objects:
#         for object_rect in objects:
#             if player.colliderect(object_rect):

def items_collisions_with_remove(player, objects):
    if objects:
        for object_rect in objects:
            if player.colliderect(object_rect):
                objects.remove(object_rect)
                return True
    return False

def items_collisions_without_remove(player, objects):
    if objects:
        for object_rect in objects:
            if player.colliderect(object_rect):
                return True
    return False

def player_animation():
    global player_surf, player_index, player_walk_1, player_walk_2, player_jump, player_crouch, score, current_level,\
        good_atom_spawn_count, bad_atom_spawn_count, player_walk

    if player_rect.bottom < 710:  # play walking animation if the player is on the floor
        player_surf = player_jump
    else:  # play jump animation if it is not on the floor
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


def good_atom_animation():
    global good_atom_surf, good_atom_index

    good_atom_index += 0.1
    if good_atom_index >= len(good_atom_walk):
        good_atom_index = 0
    good_atom_surf = good_atom_walk[int(good_atom_index)]


def bad_atom_animation():
    global bad_atom_surf, bad_atom_index

    bad_atom_index += 0.1
    if bad_atom_index >= len(bad_atom_walk):
        bad_atom_index = 0
    bad_atom_surf = bad_atom_walk[int(bad_atom_index)]


def proton_animation():
    global proton_surf, proton_index

    proton_index += 0.1
    if proton_index >= len(proton_fly):
        proton_index = 0
    proton_surf = proton_fly[int(proton_index)]

def proton_movement(proton_list):

    if proton_list:
        for proton_rec in proton_list:
           proton_rec.x -= 5

           screen.blit(proton_surf,proton_rec)
        
        proton_list = [proton for proton in proton_list if proton.x > -200] # delete snails that are beyond -100(x)

        return proton_list
    else:
        return []


# crear electron_animation (caballito)
def electron_animation():
    global electron_surf, electron_index

    electron_index += 0.1
    if electron_index >= len(electron_fly):
        electron_index = 0
    electron_surf = electron_fly[int(electron_index)]

def electron_movement(electron_list):

    if electron_list:
        for electron_rec in electron_list:
           electron_rec.x -= 5

           screen.blit(electron_surf,electron_rec)
        
        electron_list = [electron for electron in electron_list if electron.x > -200] # delete snails that are beyond -100(x)

        return electron_list
    else:
        return []


def portal_animation():
    global portal_surf, portal_index

    portal_index += 0.1
    if portal_index >= len(portal_movement_frames):
        portal_index = 0
    portal_surf = portal_movement_frames[int(portal_index)]


def portal_movement(portal_list):
    if portal_list:
        for portal_rec in portal_list:
            portal_rec.x -= 5

            screen.blit(portal_surf, portal_rec)

        portal_list = [portal for portal in portal_list if portal.x > -200]  # delete snails that are beyond -100(x)

        return portal_list
    else:
        return []


def check_portals_spawn():
    global portal_down, portal_up, portal_movement_frames, portal_1_already_spawned, portal_2_already_spawned, portal_3_already_spawned, game_active

    if current_level == 1 and score == 30:

        portal_down = pygame.image.load('graphics/portal/portal1up.png')
        portal_up = pygame.image.load('graphics/portal/portal1down.png')
        if not portal_1_already_spawned:
            portal_atom_rect_list.append(portal_surf.get_rect(bottomright = (randint(1500,2500),randint(100,900))))
            portal_1_already_spawned = True

    elif current_level == 2 and score == 90:

        portal_up = pygame.image.load('graphics/portal/portal2up.png')
        portal_down = pygame.image.load('graphics/portal/portal2down.png')
        if not portal_2_already_spawned:
            portal_atom_rect_list.append(portal_surf.get_rect(bottomright = (randint(1500,2500),randint(100,900))))
            portal_2_already_spawned = True

    elif current_level == 3 and score == 180:

        portal_up = pygame.image.load('graphics/portal/portal3up.png')
        portal_down = pygame.image.load('graphics/portal/portal3down.png')
        if not portal_3_already_spawned:
            portal_atom_rect_list.append(portal_surf.get_rect(bottomright = (randint(1500,2500),randint(100,900))))
            portal_3_already_spawned = True

    portal_movement_frames = [portal_up, portal_down]

def extract_good_atom_electrons():
    global collected_electron_count, electrons_number
    if collected_electron_count - 1 < 0:
        collected_electron_count = 0
    else:
        collected_electron_count -= 1
    electrons_number = test_font.render(str(collected_electron_count), False, 'White')


def extract_bad_atom_electrons():
    global collected_electron_count, electrons_number

    if collected_electron_count - 6 < 0:
        collected_electron_count = 0
    else:
        collected_electron_count -= 6
    electrons_number = test_font.render(str(collected_electron_count), False, 'White')

def check_current_player():
    global player_walk_1, player_walk_2, player_jump, player_crouch, player_walk, current_level
    if current_level == 1:
        player_walk_1 = pygame.image.load('graphics/player/hydrogen_character_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/hydrogen_character_2.png').convert_alpha()
        player_jump = pygame.image.load('graphics/player/hydrogen_character_jump.png').convert_alpha()
        player_crouch = pygame.image.load('graphics/player/hydrogen_character_crouch.png')

    elif current_level == 2:
        player_walk_1 = pygame.image.load('graphics/player/sulphur_character_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/sulphur_character_2.png').convert_alpha()
        player_jump = pygame.image.load('graphics/player/sulphur_character_jump.png').convert_alpha()
        player_crouch = pygame.image.load('graphics/player/sulphur_character_crouch.png')

    elif current_level == 3:
        player_walk_1 = pygame.image.load('graphics/player/bromine_character_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/bromine_character_2.png').convert_alpha()
        player_jump = pygame.image.load('graphics/player/bromine_character_jump.png').convert_alpha()
        player_crouch = pygame.image.load('graphics/player/bromine_character_crouch.png')

    elif current_level == 4:
        player_walk_1 = pygame.image.load('graphics/player/xenon_character_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/xenon_character_2.png').convert_alpha()
        player_jump = pygame.image.load('graphics/player/xenon_character_jump.png').convert_alpha()
        player_crouch = pygame.image.load('graphics/player/xenon_character_crouch.png')
    player_walk = [player_walk_1, player_walk_2]

def check_win_lose():
    global collected_electron_count, current_level, score, collected_proton_count, game_active, portal_1_already_spawned, portal_2_already_spawned, portal_3_already_spawned

    player_lost_in_level_one = current_level == 1 and score > 30 and portal_1_already_spawned and len(portal_atom_rect_list) == 0
    player_lost_in_level_two = current_level == 2 and score > 90 and portal_2_already_spawned and len(portal_atom_rect_list) == 0
    player_lost_in_level_three = current_level == 3 and score > 180 and portal_3_already_spawned and len(portal_atom_rect_list) == 0

    if player_lost_in_level_one or player_lost_in_level_two or player_lost_in_level_three :
        game_active = False


def check_collisions():
    global protons_number, collected_electron_count, electrons_number, current_level, collected_proton_count, good_atom_1, good_atom_2, bad_atom_1, bad_atom_2

    if bad_atom_rect_list:
        if items_collisions_without_remove(player_rect, bad_atom_rect_list):
            extract_bad_atom_electrons()
    if good_atom_rect_list:
        if items_collisions_without_remove(player_rect, good_atom_rect_list):
            extract_good_atom_electrons()
    if proton_rect_list:
        if items_collisions_with_remove(player_rect, proton_rect_list):
            collected_proton_count += 1
            protons_number = test_font.render(str(collected_proton_count), False, 'White')
    if electron_rect_list:
        if items_collisions_with_remove(player_rect, electron_rect_list):
            collected_electron_count += 1
            electrons_number = test_font.render(str(collected_electron_count), False, 'White')
    if portal_atom_rect_list:
        if items_collisions_without_remove(player_rect, portal_atom_rect_list):
            if (config[current_level]["total_electrons_needed"] == collected_electron_count and
                    config[current_level]["total_protons_needed"] == collected_proton_count):
                current_level += 1
                portal_atom_rect_list.clear()


def check_player_ground_limits():
    global player_rect, player_gravity

    player_gravity += 1
    player_rect.y += player_gravity

    if ground_1[0] < player_rect.x < ground_1[1]:
        if player_rect.bottom >= 710:
            player_rect.bottom = 710
    if ground_2[0] < player_rect.x < ground_2[1]:
        if player_rect.bottom >= 850:
            player_rect.bottom = 850
    if ground_3[0] < player_rect.x < ground_3[1]:
        if player_rect.bottom >= 730:
            player_rect.bottom = 730
    if ground_4[0] < player_rect.x < ground_4[1]:
        if player_rect.bottom >= 610:
            player_rect.bottom = 610
    # elif ground_1[1] < player_rect.x < ground_2[0] and jump == False:
    #     player_gravity = 1
    # elif ground_2[1] < player_rect.x < ground_3[0] and jump == False:
    #     player_gravity = 1
    # elif ground_3[1] < player_rect.x < ground_4[0] and jump == False:
    #     player_gravity = 1    
    else:
        if jump == False:
            player_rect.midbottom = (player_rect.midbottom[0], player_rect.midbottom[1])
            player_gravity = 15 

    screen.blit(player_surf, player_rect)


# Setup
pygame.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH,
                                  SCREEN_HEIGHT))  # Create screen. This code ends, so to keep it running we use the while True (is never False).
pygame.display.set_caption('Monster Arena')
clock = pygame.time.Clock()  # clock object to handle frame rate
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
current_level = 1

is_changing_level = False

# Surfaces
sky_surface = pygame.image.load('graphics/sky.png').convert_alpha()
sky_surface_width = sky_surface.get_width()

sky_background_surface = pygame.image.load('graphics/sky-background.png').convert()

# Define game variables
scroll_sky_background = 0
scroll_sky = 0
tiles = math.ceil(SCREEN_WIDTH / sky_surface_width) + 1

ground_sur_1 = pygame.image.load('graphics/ground/ground-1.png').convert_alpha()
ground_sur_1 = pygame.transform.rotozoom(ground_sur_1, 0, 1.3)
ground_sur_2 = pygame.image.load('graphics/ground/ground-2.png').convert_alpha()
ground_sur_2 = pygame.transform.rotozoom(ground_sur_2, 0, 1.3)
ground_sur_3 = pygame.image.load('graphics/ground/ground-3.png').convert_alpha()
ground_sur_3 = pygame.transform.rotozoom(ground_sur_3, 0, 1.3)
ground_sur_4 = pygame.image.load('graphics/ground/ground-4.png').convert_alpha()
ground_sur_4 = pygame.transform.rotozoom(ground_sur_4, 0, 1.3)

ground_sur_1_rect = ground_sur_1.get_rect(center=(100, 100))
ground_sur_2_rect = ground_sur_2.get_rect(center=(100, 100))
ground_sur_3_rect = ground_sur_3.get_rect(center=(100, 100))
ground_sur_4_rect = ground_sur_4.get_rect(center=(100, 100))

# UI
timer = pygame.image.load('graphics/UI/timer.png')
timer_rect = timer.get_rect(center = (0,0))
timer = pygame.transform.rotozoom(timer,0,0.8)
timer_charging = pygame.image.load('graphics/UI/charging.png')
timer_charging = pygame.transform.rotozoom(timer_charging,0,0.8)

hidden_sulfur = pygame.image.load('graphics/UI/hidden-sulfur.png')
hidden_sulfur = pygame.transform.rotozoom(hidden_sulfur,0,0.8)
hidden_bromine = pygame.image.load('graphics/UI/hidden-bromine.png')
hidden_bromine = pygame.transform.rotozoom(hidden_bromine,0,0.8)
hidden_xenon = pygame.image.load('graphics/UI/hidden-xenon.png')
hidden_xenon = pygame.transform.rotozoom(hidden_xenon,0,0.8)

protons_bar_sur = pygame.image.load('graphics/UI/protons_bar.png')
protons_bar_sur = pygame.transform.rotozoom(protons_bar_sur,0,0.5)
protons_bar_rect = protons_bar_sur.get_rect(center = (100,100))
collected_proton_count = 0

electrons_bar_sur = pygame.image.load('graphics/UI/electrons_bar.png')
electrons_bar_sur = pygame.transform.rotozoom(electrons_bar_sur,0,0.5)
electrons_bar_rect = electrons_bar_sur.get_rect(center = (100,100))
collected_electron_count = 0

# Enemies
good_atom_1 = pygame.image.load('graphics/atoms/good_atom1_light.png').convert_alpha()
good_atom_2 = pygame.image.load('graphics/atoms/good_atom2_light.png').convert_alpha()
good_atom_index = 0
good_atom_walk = [good_atom_1, good_atom_2]
good_atom_surf = good_atom_walk[good_atom_index]

good_atom_spawn_count = 0
good_atom_rect_list = []

bad_atom_1 = pygame.image.load('graphics/atoms/bad_atom1_light.png').convert_alpha()
bad_atom_1 = pygame.transform.rotozoom(bad_atom_1, 0, 0.5)
bad_atom_2 = pygame.image.load('graphics/atoms/bad_atom2_light.png').convert_alpha()
bad_atom_2 = pygame.transform.rotozoom(bad_atom_2, 0, 0.5)
bad_atom_index = 0
bad_atom_walk = [bad_atom_1, bad_atom_2]
bad_atom_surf = bad_atom_walk[bad_atom_index]

bad_atom_rect_list = []
bad_atom_spawn_count = 0

# Items
proton_1 = pygame.image.load('graphics/items/proton1.png')
proton_1 = pygame.transform.rotozoom(proton_1,0,0.7)
proton_2 = pygame.image.load('graphics/items/proton2.png')
proton_2 = pygame.transform.rotozoom(proton_2,0,0.7)
proton_fly = [proton_1,proton_2]
proton_index = 0
proton_surf = proton_fly[proton_index]

proton_rect_list = []
proton_spawn_count = 0

proton_rect = proton_surf.get_rect(center = (100,100))

electron_1 = pygame.image.load('graphics/items/electron1.png')
electron_1 = pygame.transform.rotozoom(electron_1,0,0.7)
electron_2 = pygame.image.load('graphics/items/electron2.png')
electron_2 = pygame.transform.rotozoom(electron_2,0,0.7)
electron_fly = [electron_1,electron_2]
electron_index = 0
electron_surf = electron_fly[electron_index]

electron_rect_list = []
electron_spawn_count = 0

electron_rect = electron_surf.get_rect(center = (100,100))

# Player Characters
player_walk_1 = pygame.image.load('graphics/player/hydrogen_character_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/hydrogen_character_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_crouch = pygame.image.load('graphics/Player/hydrogen_character_crouch.png')
player_index = 0
player_surf = player_walk[player_index]
player_jump = pygame.image.load('graphics/player/hydrogen_character_jump.png').convert_alpha()

player_rect = player_surf.get_rect(midbottom = (0,0))
player_gravity = 0

# Intro Screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)  # overwrites variable to scale image
player_stand_rect = player_stand.get_rect(center=(960, 500))

# text
title_surf = test_font.render('Monster Arena', False, 'White')
title_rect = title_surf.get_rect(center=(960, 100))

instructions = test_font.render('Press space to start',False,'White')
instructions_rect = instructions.get_rect(center = (960,630))

protons_number = test_font.render(str(collected_proton_count),False,'White')
protons_number_rect = protons_number.get_rect(center = (0,0))

electrons_number = test_font.render(str(collected_electron_count),False,'White')
electrons_number_rect = electrons_number.get_rect(center = (0,0))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Portals
portal_up = pygame.image.load('graphics/portal/portal1up.png')
portal_down = pygame.image.load('graphics/portal/portal1down.png')
portal_movement_frames = [portal_up, portal_down]
portal_index = 0
portal_surf = portal_movement_frames[portal_index]

portal_atom_rect_list = []

running = True

jump = False
move_right = False
move_left = False
crouch = False

portal_1_already_spawned = False
portal_2_already_spawned = False
portal_3_already_spawned = False



while running:  # The game will be continuously updated.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if (player_rect.bottom == 710 or player_rect.bottom == 850 or player_rect.bottom == 730 or player_rect.bottom == 610) and (event.key == pygame.K_SPACE or event.key == pygame.K_w):
                    player_gravity = -25
                    jump = True
                if event.key == pygame.K_a:
                    move_left = True
                if event.key == pygame.K_d:
                    move_right = True
                if event.key == pygame.K_s:
                    crouch = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    jump = False
                if event.key == pygame.K_a:
                    move_left = False
                if event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_s:
                    crouch = False

            if move_left:
                player_rect.right -= 15
                if player_rect.right <= 140:
                    player_rect.right = 140
            if move_right:
                player_rect.right += 15
                if player_rect.right >= 1920:
                    player_rect.right = 1920
            if current_level == 3:
                if move_right:
                    player_rect.right += 20
                if move_left:
                    player_rect.right -= 20

            player_animation()

            if crouch:
                player_surf = player_crouch
            if player_surf == player_crouch:
                player_rect = player_surf.get_rect(midbottom = (player_rect.midbottom[0],760))
                player_rect = player_surf.get_rect(midbottom = (player_rect.midbottom))

            if not crouch and player_rect.midbottom[1] < 711 and jump == False:
                player_rect = player_surf.get_rect(midbottom=(player_rect.midbottom[0], 710))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            if good_atom_spawn_count <= config[current_level]["good_atoms"] and not good_atom_rect_list:
                good_atom_1 = pygame.image.load('graphics/atoms/good_atom1_light.png').convert_alpha()
                good_atom_2 = pygame.image.load('graphics/atoms/good_atom2_light.png').convert_alpha()
                good_atom_rect_list.append(good_atom_surf.get_rect(bottomright = (randint(1500,2500),randint(350,850))))
                good_atom_spawn_count += 1

            if bad_atom_spawn_count <= config[current_level]["bad_atoms"] and not bad_atom_rect_list:
                bad_atom_rect_list.append(bad_atom_surf.get_rect(bottomright = (randint(1500,2500),randint(350,850))))
                bad_atom_spawn_count += 1

            if electron_spawn_count <= config[current_level]["electrons"] and not electron_rect_list:
                electron_rect_list.append(electron_surf.get_rect(bottomright = (randint(1500,2500),randint(350,850))))
                electron_spawn_count += 1

            if proton_spawn_count <= config[current_level]["protons"] and not proton_rect_list:
                proton_rect_list.append(proton_surf.get_rect(bottomright = (randint(1500,2500),randint(350,850))))
                proton_spawn_count += 1

            check_portals_spawn()

    if game_active:
        # SKY BACKGROUND SURFACE
        for i in range(0, tiles):
            screen.blit(sky_background_surface, (i * sky_surface_width + scroll_sky_background, 110))
        # scrolling sky_surface background and reseting
        scroll_sky_background -= 3
        if abs(scroll_sky_background) > sky_surface_width:
            scroll_sky_background = 0

        # SKY SURFACE
        for i in range(0, tiles):
            screen.blit(sky_surface, (i * sky_surface_width + scroll_sky, 0))
        # scrolling sky_surface background and reseting
        scroll_sky -= 5
        if abs(scroll_sky) > sky_surface_width:
            scroll_sky = 0

        ground_1 = (0,380)
        ground_2 = (500,820)
        ground_3 = (950,1170)
        ground_4 = (1260,1950)

        screen.blit(ground_sur_1,(0,710))
        screen.blit(ground_sur_2,(550,850))
        screen.blit(ground_sur_3,(1000,730))
        screen.blit(ground_sur_4,(1300,610))

        pygame.draw.line(screen, (255,0,0), (0,850), (1920,850), 1)
        pygame.draw.line(screen, (255,0,0), (0,320), (1920,320), 1)

        check_current_player()
    
        # BARS
        screen.blit(timer_charging,(200,0))
        screen.blit(timer,(200,0))
        screen.blit(hidden_sulfur,(200,0))
        screen.blit(hidden_bromine,(200,0))
        screen.blit(hidden_xenon,(200,0))
        
        screen.blit(protons_bar_sur, (760,120))
        screen.blit(electrons_bar_sur, (760,200))
        screen.blit(protons_number,(1090,160))
        screen.blit(electrons_number,(1090,242))

        score = displayScore()

        check_player_ground_limits()

        # morir por caida
        if player_rect.midbottom[1] > 1200:
            game_active = False

        # Obstacle movement
        bad_atom_rect_list = bad_atom_movement(bad_atom_rect_list)
        good_atom_rect_list = good_atom_movement(good_atom_rect_list)
        portal_atom_rect_list = portal_movement(portal_atom_rect_list)

        good_atom_animation()
        bad_atom_animation()

        # Items
        electron_rect_list = electron_movement(electron_rect_list)
        proton_rect_list = proton_movement(proton_rect_list)

        proton_animation()
        electron_animation()

        # Collisions
        check_collisions()
        # Portals
        portal_animation()

        # Win / Lose
        check_win_lose()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title_surf, title_rect)
        bad_atom_rect_list.clear()
        player_rect.midbottom = (80, 710)

        player_gravity = 0
        move_left = False
        move_right = False
        crouch = False
        jump = False
        collected_electron_count = 0
        collected_proton_count = 0

        score_message = test_font.render(f'Your score: {score}',False,'White')
        score_message_rect = score_message.get_rect(center = (960,400))

        if score == 0:
            screen.blit(instructions, instructions_rect)
        else:
            screen.blit(score_message,score_message_rect)
        
    pygame.display.update() # update the screen
    clock.tick(60) # while True runs 60 times per second
