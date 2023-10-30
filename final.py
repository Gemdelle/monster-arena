import pygame
from sys import exit # to exit the game without having issues with the True loop

# Basic Setup
# Surfaces

pygame.init()
screen = pygame.display.set_mode((800,400)) # Create screen. This code ends, so to keep it running we use the while True (is never False).
pygame.display.set_caption('Monster Arena')
clock = pygame.time.Clock() # clock object to handle frame rate

text_surface = pygame.Surface()

while True: # The game will be continuously updated.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit()
    pygame.display.update() # update the screen
    clock.tick(60) # while True runs 60 times per second