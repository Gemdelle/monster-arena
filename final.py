import pygame
from sys import exit # to exit the game without having issues with the True loop

# 01. Basic Setup
# 02. Surfaces

# Setup
pygame.init()
screen = pygame.display.set_mode((800,400)) # Create screen. This code ends, so to keep it running we use the while True (is never False).
pygame.display.set_caption('Monster Arena')
clock = pygame.time.Clock() # clock object to handle frame rate
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# Surfaces
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

score_surf = test_font.render('Monster Arena', False, (64,64,64)) # text, antianaliser, color.
score_rect = score_surf.get_rect(center = (400,50))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (600,300))

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(bottomright = (100,300))
player_gravity = 0

while True: # The game will be continuously updated.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit()
        if event.type == pygame.MOUSEMOTION:
            if player_rect.bottom == 300 and player_rect.collidepoint(event.pos):
                player_gravity = -20

        if event.type == pygame.KEYDOWN:
            if player_rect.bottom == 300 and event.key == pygame.K_SPACE:
                    player_gravity = -20

    screen.blit(sky_surface,(0,0)) # block image transfer -> to display images in screen
    screen.blit(ground_surface,(0,300))

    pygame.draw.rect(screen,'#c0e8ec',score_rect)
    pygame.draw.rect(screen,'#c0e8ec',score_rect,12)
    screen.blit(score_surf,score_rect)

    # Snail
    screen.blit(snail_surface,snail_rect)
    snail_rect.x -= 5
    if snail_rect.left <= -50:
        snail_rect.right = 850

    # Player
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= 300:
         player_rect.bottom = 300
    screen.blit(player_surface,player_rect)

    # Collision
    if snail_rect.colliderect(player_rect):
         pygame.quit()

    pygame.display.update() # update the screen
    clock.tick(60) # while True runs 60 times per second

    # Extra things -----------------------------------------------------------------------------------------------
    #     pygame.draw.line(screen,'Black',(0,0),pygame.mouse.get_pos(),2)

        # Keys
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    #     print('jump')

    # if player_rect.colliderect(snail_rect):
    #     print('collision')
    # else:
    #     print('Free')

    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     print('collision')
    # else:
    #     print('no collision')