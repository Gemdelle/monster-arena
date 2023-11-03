import pygame
from sys import exit # to exit the game without having issues with the True loop
from random import randint

# 01. Basic Setup
# 02. Surfaces

def displayScore():
    current_time = (int(pygame.time.get_ticks() / 1000) - start_time) 
    score_surf = test_font.render(str(current_time),False,(64,4,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)

    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rec in obstacle_list:
            obstacle_rec.x -= 5

            if obstacle_rec.bottom == 300:
                screen.blit(snail_surf,obstacle_rec)
            else:
                screen.blit(fly_surf,obstacle_rec)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] # delete snails that are beyond -100(x)

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
    global player_surf, player_index
        
    if player_rect.bottom < 300: # play walking animation if the player is on the floor
        player_surf = player_jump
    else: # play jump animation if it is not on the floor
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

def snail_animation():
    global snail_surf, snail_index

    snail_index += 0.1
    if snail_index >= len(snail_walk):
        snail_index = 0
    snail_surf = snail_walk[int(snail_index)]

def fly_animation():
    global fly_surf, fly_index

    fly_index += 0.1
    if fly_index >= len(fly_fly):
        fly_index = 0
    fly_surf = fly_fly[int(fly_index)]

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

# Obstacles
snail_walk_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_walk_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_index = 0
snail_walk = [snail_walk_1,snail_walk_2]
snail_surf = snail_walk[snail_index]

fly_fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_index = 0
fly_fly = [fly_fly_1,fly_fly_2]
fly_surf = fly_fly[fly_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load('graphics/player/sulphur_character_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/sulphur_character_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_surf = player_walk[player_index]
player_jump = pygame.image.load('graphics/player/sulphur_character_jump.png').convert_alpha()

player_rect = player_surf.get_rect(bottomright = (100,300))
player_gravity = 0

# Intro Screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2) # overwrites variable to scale image 
player_stand_rect = player_stand.get_rect(center = (400,200))

# text
title_surf = test_font.render('Monster Arena',False, 'White')
title_rect = title_surf.get_rect(center = (400,70))

instructions = test_font.render('Press space to start',False,'White')
instructions_rect = instructions.get_rect(center = (400,330))

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
            if event.type == pygame.MOUSEMOTION:
                if player_rect.bottom == 450 and player_rect.collidepoint(event.pos):
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if player_rect.bottom == 450 and event.key == pygame.K_SPACE:
                        player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300))) 
            else:
                obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),randint(80,220)))) 

    if game_active:
        screen.blit(sky_surface,(0,0)) # block image transfer -> to display images in screen
        screen.blit(ground_surface,(0,450))

        score = displayScore()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 450:
            player_rect.bottom = 450
        player_animation()
        screen.blit(player_surf,player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        snail_animation()
        fly_animation()

        # Collisions
        game_active = collisions(player_rect,obstacle_rect_list)

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(title_surf,title_rect)
        obstacle_rect_list.clear()
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
