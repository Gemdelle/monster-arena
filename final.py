import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400)) # Create screen. This code ends, so to keep it running we use the while True (is never False).

while True: # The game will be continuously updated.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
    pygame.display.update() # update the screen
