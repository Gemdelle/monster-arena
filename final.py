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
text_surface = test_font.render('Monster Arena', False, 'Black') # text, antianaliser, color.

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (600,300))

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(bottomright = (600,300))

while True: # The game will be continuously updated.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit()

    screen.blit(sky_surface,(0,0)) # block image transfer -> to display images in screen
    screen.blit(ground_surface,(0,300))
    screen.blit(text_surface,(300,50))
    screen.blit(snail_surface,snail_rect)
    snail_rect.x -= 3
    if snail_rect.left <= -50:
        snail_rect.right = 850
    screen.blit(player_surface,player_rect)

    if player_rect.colliderect(snail_rect):
        print('collision')
    else:
        print('Free')

    pygame.display.update() # update the screen
    clock.tick(60) # while True runs 60 times per second