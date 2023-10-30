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
sky_surface = pygame.image.load('graphics/Sky.png')
ground_surface = pygame.image.load('graphics/ground.png')
text_surface = test_font.render('Monster Arena', False, 'Black') # text, antianaliser, color.

snail_surface = pygame.image.load('graphics/snail/snail1.png')
snail_x_position = 600

while True: # The game will be continuously updated.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit()

    screen.blit(sky_surface,(0,0)) # block image transfer -> to display images in screen
    screen.blit(ground_surface,(0,300))
    screen.blit(text_surface,(300,50))
    screen.blit(snail_surface,(snail_x_position,265))

    snail_x_position -= 4
    if snail_x_position < -50:
        snail_x_position = 850

    pygame.display.update() # update the screen
    clock.tick(60) # while True runs 60 times per second