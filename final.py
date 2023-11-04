import pygame
from sys import exit # to exit the game without having issues with the True loop
from random import randint
import math

from Config.config import config


# 01. Basic Setup
# 02. Surfaces

def displayScore():
    current_time = (int(pygame.time.get_ticks() / 1000) - start_time) 
    score_surf = test_font.render(str(current_time),False,'White')
    score_rect = score_surf.get_rect(center = (960,100))
    screen.blit(score_surf,score_rect)

    return current_time

def bad_atom_movement(obstacle_list):
    global bad_atom_spawn_count

    if obstacle_list:
        for obstacle_rec in obstacle_list:
            obstacle_rec.x -= 5

            if obstacle_rec.bottom <= 300:
                screen.blit(bad_atom_surf,obstacle_rec)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -200] # delete snails that are beyond -100(x)

        return obstacle_list
    else:
        return []

def good_atom_movement(obstacle_list):
    global good_atom_spawn_count

    if obstacle_list:
        for obstacle_rec in obstacle_list:
            obstacle_rec.x -= 5

            if obstacle_rec.bottom <= 300:
                screen.blit(good_atom_surf,obstacle_rec)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -200] # delete snails that are beyond -100(x)

        return obstacle_list
    else:
        return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surf, player_index, player_walk_1,player_walk_2,player_jump, player_crouch, score, current_level, good_atom_spawn_count, bad_atom_spawn_count, player_walk
    
    if player_rect.bottom < 710: # play walking animation if the player is on the floor
        player_surf = player_jump
    else: # play jump animation if it is not on the floor
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

# crear electron_animation (caballito)
def electron_animation():
    global electron_surf, electron_index

    electron_index += 0.1
    if electron_index >= len(electron_fly):
        electron_index = 0
    electron_surf = electron_fly[int(electron_index)]

def electron_movement(obstacle_list):
   
    if obstacle_list:
        for obstacle_rec in obstacle_list:
            obstacle_rec.x -= 5

            if obstacle_rec.bottom <= 300:
                screen.blit(electron_surf,obstacle_rec)
          
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -200] # delete snails that are beyond -100(x)

        return obstacle_list
    else:
        return []

def portal_animation():
    global portal_surf, portal_index

    portal_index += 0.1
    if portal_index >= len(portal_movement):
        portal_index = 0
    portal_surf = portal_movement[int(portal_index)] 

def portalMovement():
    portal_rect.x -= 5
    if portal_rect.midbottom > (-200,660): 
        screen.blit(portal_surf, portal_rect)
    if portal_rect.midbottom < (-200,660):
        portal_rect.midbottom = (2000,660)
    
# Setup
pygame.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) # Create screen. This code ends, so to keep it running we use the while True (is never False).
pygame.display.set_caption('Monster Arena')
clock = pygame.time.Clock() # clock object to handle frame rate
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
current_level = 1

is_changing_level = False

# Surfaces
sky_surface = pygame.image.load('graphics/sky.png').convert_alpha()
# sky_surface = pygame.transform.rotozoom(sky_surface,0,1.2)
sky_surface_width = sky_surface.get_width()

sky_background_surface = pygame.image.load('graphics/sky-background.png').convert()
# sky_background_surface = pygame.transform.rotozoom(sky_background_surface,0,0.35)

# Define game variables
scroll_sky_background = 0
scroll_sky = 0
tiles = math.ceil(SCREEN_WIDTH / sky_surface_width) + 1

ground_sur_1 = pygame.image.load('graphics/ground/ground-1.png').convert_alpha()
ground_sur_1 = pygame.transform.rotozoom(ground_sur_1,0,1.5)
ground_sur_2 = pygame.image.load('graphics/ground/ground-2.png').convert_alpha()
ground_sur_2 = pygame.transform.rotozoom(ground_sur_2,0,1.5)
ground_sur_3 = pygame.image.load('graphics/ground/ground-3.png').convert_alpha()
ground_sur_3 = pygame.transform.rotozoom(ground_sur_3,0,1.5)

ground_sur_1_rect = ground_sur_1.get_rect(center = (100,100))
ground_sur_2_rect = ground_sur_2.get_rect(center = (100,100))
ground_sur_3_rect = ground_sur_3.get_rect(center = (100,100))

# Bars
protons_bar_sur = pygame.image.load('graphics/UI/protons_bar.png')
protons_bar_sur = pygame.transform.rotozoom(protons_bar_sur,0,0.6) 
protons_bar_rect = protons_bar_sur.get_rect(center = (100,100))

electrons_bar_sur = pygame.image.load('graphics/UI/electrons_bar.png')
electrons_bar_sur = pygame.transform.rotozoom(electrons_bar_sur,0,0.6)
electrons_bar_rect = electrons_bar_sur.get_rect(center = (100,100))

# Enemies
good_atom_1 = pygame.image.load('graphics/atoms/good_atom1.png').convert_alpha()
good_atom_2 = pygame.image.load('graphics/atoms/good_atom2.png').convert_alpha()
good_atom_index = 0
good_atom_walk = [good_atom_1,good_atom_2]
good_atom_surf = good_atom_walk[good_atom_index]

good_atom_spawn_count = 0
good_atom_rect_list = []

bad_atom_1 = pygame.image.load('graphics/atoms/bad_atom1.png').convert_alpha()
bad_atom_1 = pygame.transform.rotozoom(bad_atom_1,0,0.5)
bad_atom_2 = pygame.image.load('graphics/atoms/bad_atom2.png').convert_alpha()
bad_atom_2 = pygame.transform.rotozoom(bad_atom_2,0,0.5)
bad_atom_index = 0
bad_atom_walk = [bad_atom_1,bad_atom_2]
bad_atom_surf = bad_atom_walk[bad_atom_index]

bad_atom_rect_list = []
bad_atom_spawn_count = 0

# Items
proton_1 = pygame.image.load('graphics/items/proton1.png')
proton_2 = pygame.image.load('graphics/items/proton2.png')
proton_fly = [proton_1,proton_2]
proton_index = 0
proton_surf = proton_fly[proton_index]

proton_rect = proton_surf.get_rect(center = (100,100))

electron_1 = pygame.image.load('graphics/items/electron1.png')
electron_2 = pygame.image.load('graphics/items/electron2.png')
electron_fly = [electron_1,electron_2]
electron_index = 0
electron_surf = electron_fly[electron_index]

electron_rect = electron_surf.get_rect(center = (100,100))

# Player Characters

player_walk_1 = pygame.image.load('graphics/player/hydrogen_character_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/hydrogen_character_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_crouch = pygame.image.load('graphics/Player/hydrogen_character_crouch.png')
player_index = 0
player_surf = player_walk[player_index]
player_jump = pygame.image.load('graphics/player/hydrogen_character_jump.png').convert_alpha()


player_rect = player_surf.get_rect(midbottom = (100,450))
player_gravity = 0

# Intro Screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2) # overwrites variable to scale image 
player_stand_rect = player_stand.get_rect(center = (960,500))

# text
title_surf = test_font.render('Monster Arena',False, 'White')
title_rect = title_surf.get_rect(center = (960,100))

instructions = test_font.render('Press space to start',False,'White')
instructions_rect = instructions.get_rect(center = (960,630))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

# Portals
portal_up = pygame.image.load('graphics/portal/portal1up.png')
portal_down = pygame.image.load('graphics/portal/portal1down.png')
portal_movement = [portal_up,portal_down]
portal_index = 0
portal_surf = portal_movement[portal_index]

portal_rect = portal_surf.get_rect(midbottom = (2000,660))

running = True

jump = False
move_right = False
move_left = False
crouch = False

while running: # The game will be continuously updated.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit() 
                exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                # print(player_rect.midbottom[1],score)
                if player_rect.bottom == 710 and event.key == pygame.K_SPACE or player_rect.bottom == 710 and event.key == pygame.K_w:
                    player_gravity = -25
                    print(player_rect.midbottom[1])
                    jump = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    jump = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    move_left = True
                if event.key == pygame.K_d:
                    move_right = True 
                if event.key == pygame.K_s:
                    crouch = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    move_left = False
                if  event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_s:
                    crouch = False

            if move_left:
                player_rect.right -= 10
                if player_rect.right <= 140:
                    player_rect.right = 140
            if move_right:
                player_rect.right += 10
                if player_rect.right >= 1190:
                    player_rect.right = 1190
            if score > 20 and score <= 30:
                if move_right:
                    player_rect.right += 14
                if move_left:
                    player_rect.right -= 14
            player_animation()

            if crouch:
                player_surf = player_crouch
            if player_surf == player_crouch:
                player_rect = player_surf.get_rect(midbottom = (player_rect.midbottom[0],760))
                player_rect = player_surf.get_rect(midbottom = (player_rect.midbottom))
                print(player_rect.midbottom[1])
            
            if not crouch and player_rect.midbottom[1] < 711 and jump == False:
                player_rect = player_surf.get_rect(midbottom = (player_rect.midbottom[0],710))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True 
                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            if good_atom_spawn_count <= config[current_level]["good_atoms"] and not good_atom_rect_list:
                good_atom_rect_list.append(good_atom_surf.get_rect(bottomright = (randint(1500,2500),200)))
                good_atom_spawn_count += 1
                print("good_atom_spawn_count ", good_atom_spawn_count)

            if bad_atom_spawn_count <= config[current_level]["bad_atoms"] and not bad_atom_rect_list:
                bad_atom_rect_list.append(bad_atom_surf.get_rect(bottomright = (randint(1500,2500),randint(80,220))))
                bad_atom_spawn_count += 1
                print("bad_atom_spawn_count ", bad_atom_spawn_count)

            if score < 10:
                player_walk_1 = pygame.image.load('graphics/player/hydrogen_character_1.png').convert_alpha()
                player_walk_2 = pygame.image.load('graphics/player/hydrogen_character_2.png').convert_alpha()
                player_jump = pygame.image.load('graphics/player/hydrogen_character_jump.png').convert_alpha()
                player_crouch = pygame.image.load('graphics/player/hydrogen_character_crouch.png')
                current_level = 1

            elif 10 < score <= 20:
                player_walk_1 = pygame.image.load('graphics/player/sulphur_character_1.png').convert_alpha()
                player_walk_2 = pygame.image.load('graphics/player/sulphur_character_2.png').convert_alpha()
                player_jump = pygame.image.load('graphics/player/sulphur_character_jump.png').convert_alpha()
                player_crouch = pygame.image.load('graphics/player/sulphur_character_crouch.png')
                portal_down = pygame.image.load('graphics/portal/portal1up.png')
                portal_up = pygame.image.load('graphics/portal/portal1down.png')
                current_level = 2

            elif 20 < score <= 30:
                player_walk_1 = pygame.image.load('graphics/player/bromine_character_1.png').convert_alpha()
                player_walk_2 = pygame.image.load('graphics/player/bromine_character_2.png').convert_alpha()
                player_jump = pygame.image.load('graphics/player/bromine_character_jump.png').convert_alpha()
                player_crouch = pygame.image.load('graphics/player/bromine_character_crouch.png')
                portal_up = pygame.image.load('graphics/portal/portal2up.png')
                portal_down = pygame.image.load('graphics/portal/portal2down.png')
                current_level = 3

            elif score > 30:
                player_walk_1 = pygame.image.load('graphics/player/xenon_character_1.png').convert_alpha()
                player_walk_2 = pygame.image.load('graphics/player/xenon_character_2.png').convert_alpha()
                player_jump = pygame.image.load('graphics/player/xenon_character_jump.png').convert_alpha()
                player_crouch = pygame.image.load('graphics/player/xenon_character_crouch.png')
                portal_up = pygame.image.load('graphics/portal/portal3up.png')
                portal_down = pygame.image.load('graphics/portal/portal3down.png')
                current_level = 4

            player_walk = [player_walk_1, player_walk_2]
            portal_movement = [portal_up,portal_down]            


    if game_active:
        # SKY BACKGROUND SURFACE
        for i in range(0,tiles):
            screen.blit(sky_background_surface,(i * sky_surface_width + scroll_sky_background,110))
        # scrolling sky_surface background and reseting
        scroll_sky_background -= 3
        if abs(scroll_sky_background) > sky_surface_width:
            scroll_sky_background = 0

        # SKY SURFACE
        for i in range(0,tiles):
            screen.blit(sky_surface,(i * sky_surface_width + scroll_sky,0))
        # scrolling sky_surface background and reseting
        scroll_sky -= 5
        if abs(scroll_sky) > sky_surface_width:
            scroll_sky = 0

        screen.blit(ground_sur_1,(0,510))
        screen.blit(ground_sur_2,(600,810))
        screen.blit(ground_sur_3,(1300,610))

        # BARS
        screen.blit(protons_bar_sur, (50,50))
        screen.blit(electrons_bar_sur, (50,150))

        score = displayScore()
        
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 710:
            player_rect.bottom = 710
        screen.blit(player_surf,player_rect)

        # Obstacle movement
        bad_atom_rect_list = bad_atom_movement(bad_atom_rect_list)
        good_atom_rect_list = good_atom_movement(good_atom_rect_list)
        good_atom_animation()
        bad_atom_animation()

        # Items
        proton_animation()

        # Collisions
        game_active = collisions(player_rect,bad_atom_rect_list)

        # Portals

        if 10 < score < 20:
            portalMovement()
        elif 20 < score <= 30:
            portalMovement()
        elif 30 < score <= 40:
            portalMovement()

        portal_animation()

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(title_surf,title_rect)
        bad_atom_rect_list.clear()
        player_rect.midbottom = (80,710)

        player_gravity = 0

        score_message = test_font.render(f'Your score: {score}',False,'White')
        score_message_rect = score_message.get_rect(center = (960,540))

        if score == 0:
            screen.blit(instructions,instructions_rect)
        else:
            screen.blit(score_message,score_message_rect)
        

    pygame.display.update() # update the screen
    clock.tick(60) # while True runs 60 times per second
