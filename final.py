import pygame
from sys import exit # to exit the game without having issues with the True loop
from random import randint

# 01. Basic Setup
# 02. Surfaces

def displayScore():
    current_time = (int(pygame.time.get_ticks() / 1000) - start_time) 
    score_surf = test_font.render(str(current_time),False,(64,4,64))
    score_rect = score_surf.get_rect(center = (600,50))
    screen.blit(score_surf,score_rect)

    return current_time

def bad_atom_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rec in obstacle_list:
            obstacle_rec.x -= 5

            if obstacle_rec.bottom <= 300:
                screen.blit(bad_atom_surf,obstacle_rec)

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
    global player_surf, player_index, player_walk_1,player_walk_2,player_jump, score
    
    if score < 10:
        player_walk_1 = pygame.image.load('graphics/player/hydrogen_character_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/hydrogen_character_2.png').convert_alpha()
        player_jump = player_jump = pygame.image.load('graphics/player/hydrogen_character_jump.png').convert_alpha()
    elif score > 10 and score <= 20:
        player_walk_1 = pygame.image.load('graphics/player/sulphur_character_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/sulphur_character_2.png').convert_alpha()
        player_jump = player_jump = pygame.image.load('graphics/player/sulphur_character_jump.png').convert_alpha()
        player_rect.midbottom = (80,410)

    elif score > 20 and score <= 30:
        player_walk_1 = pygame.image.load('graphics/player/bromine_character_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/bromine_character_2.png').convert_alpha()
        player_jump = player_jump = pygame.image.load('graphics/player/bromine_character_jump.png').convert_alpha()
        player_rect.midbottom = (80,450)

    elif score > 30:
        player_walk_1 = pygame.image.load('graphics/player/xenon_character_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/xenon_character_2.png').convert_alpha()
        player_jump = player_jump = pygame.image.load('graphics/player/xenon_character_jump.png').convert_alpha()
        player_rect.midbottom = (80,430)


    player_walk = [player_walk_1,player_walk_2]
    # player_surf = player_walk[player_index]
    # player_rect = player_surf.get_rect(bottomright = (100,300))

    if player_rect.bottom < 300: # play walking animation if the player is on the floor
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

# Setup
pygame.init()
screen = pygame.display.set_mode((1200,650)) # Create screen. This code ends, so to keep it running we use the while True (is never False).
pygame.display.set_caption('Monster Arena')
clock = pygame.time.Clock() # clock object to handle frame rate
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

# Surfaces
sky_surface = pygame.image.load('graphics/Sky.png').convert()
sky_surface = pygame.transform.rotozoom(sky_surface,0,1.5)
ground_surface = pygame.image.load('graphics/ground.png').convert()
ground_surface = pygame.transform.rotozoom(ground_surface,0,1.5)

# Enemies
good_atom_1 = pygame.image.load('graphics/atoms/good_atom1.png').convert_alpha()
good_atom_2 = pygame.image.load('graphics/atoms/good_atom2.png').convert_alpha()
good_atom_index = 0
good_atom_walk = [good_atom_1,good_atom_2]
good_atom_surf = good_atom_walk[good_atom_index]

bad_atom_1 = pygame.image.load('graphics/atoms/bad_atom1.png').convert_alpha()
bad_atom_1 = pygame.transform.rotozoom(bad_atom_1,0,2)
bad_atom_2 = pygame.image.load('graphics/atoms/bad_atom2.png').convert_alpha()
bad_atom_2 = pygame.transform.rotozoom(bad_atom_2,0,2)
bad_atom_index = 0
bad_atom_walk = [bad_atom_1,bad_atom_2]
bad_atom_surf = bad_atom_walk[bad_atom_index]

bad_atom_rect_list = []

# Items
proton_1 = pygame.image.load('graphics/items/proton1.png')
proton_2 = pygame.image.load('graphics/items/proton2.png')
proton_fly = [proton_1,proton_2]
proton_index = 0
proton_surf = proton_fly[proton_index]

proton_rect = proton_surf.get_rect(center = (100,100))

# Player Characters

player_walk_1 = pygame.image.load('graphics/player/bromine_character_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/bromine_character_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_surf = player_walk[player_index]
player_jump = pygame.image.load('graphics/player/bromine_character_jump.png').convert_alpha()

player_rect = player_surf.get_rect(bottomright = (100,300))
player_gravity = 0

# Intro Screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2) # overwrites variable to scale image 
player_stand_rect = player_stand.get_rect(center = (600,300))

# text
title_surf = test_font.render('Monster Arena',False, 'White')
title_rect = title_surf.get_rect(center = (600,70))

instructions = test_font.render('Press space to start',False,'White')
instructions_rect = instructions.get_rect(center = (600,430))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

running = True

while running: # The game will be continuously updated.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.type == pygame.K_ESCAPE:
            pygame.quit() 
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if player_rect.bottom == 450 and event.key == pygame.K_SPACE:
                        player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                bad_atom_rect_list.append(good_atom_surf.get_rect(bottomright = (randint(1100,1500),200))) 
            else:
                bad_atom_rect_list.append(bad_atom_surf.get_rect(bottomright = (randint(1100,1500),randint(80,220)))) 

    if game_active:
        screen.blit(sky_surface,(0,0)) # block image transfer -> to display images in screen
        screen.blit(ground_surface,(0,450))

        score = displayScore()
        
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 450:
            player_rect.bottom = 450
        player_animation()
        screen.blit(player_surf,player_rect)

        # Obstacle movement
        bad_atom_rect_list = bad_atom_movement(bad_atom_rect_list)

        good_atom_animation()
        bad_atom_animation()

        # Itemas
        proton_animation()

        # Collisions
        game_active = collisions(player_rect,bad_atom_rect_list)

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(title_surf,title_rect)
        bad_atom_rect_list.clear()
        player_rect.midbottom = (80,450)
        player_rect.midbottom = (80,450)

        player_gravity = 0

        score_message = test_font.render(f'Your score: {score}',False,'White')
        score_message_rect = score_message.get_rect(center = (400,330))

        if score == 0:
            screen.blit(instructions,instructions_rect)
        else:
            screen.blit(score_message,score_message_rect)
        

    pygame.display.update() # update the screen
    clock.tick(60) # while True runs 60 times per second
