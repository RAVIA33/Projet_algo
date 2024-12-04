import pygame
# Import all pygame modules
# pygame MUST be installed before via 'pip install pygame'
from typing import Tuple


WINDOW_SIZE: Tuple[int, int]  = (480, 360)
# Define pygame window size in pixels

pygame.init()
# Initialize all imported pygame modules
# https://www.pygame.org/docs/ref/pygame.html#pygame.init

flags: pygame.constants = pygame.NOFRAME | pygame.RESIZABLE
'''
pygame.FULLSCREEN    create a fullscreen display
pygame.DOUBLEBUF     only applicable with OPENGL
pygame.HWSURFACE     (obsolete in pygame 2) hardware accelerated, only in FULLSCREEN
pygame.OPENGL        create an OpenGL-renderable display
pygame.RESIZABLE     display window should be sizeable
pygame.NOFRAME       display window will have no border or controls
pygame.SCALED        resolution depends on desktop size and scale graphics
pygame.SHOWN         window is opened in visible mode (default)
pygame.HIDDEN        window is opened in hidden mode
'''
screen: pygame.Surface = pygame.display.set_mode(WINDOW_SIZE, flags)
# Définition de l'écran, de la fenêtre
# Create a window with some special properties passed in flags
# https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode

running = True
# Initialize while loop test value
# The essential principle to understand is that
# pygame refreshes the contents of the created window
# very quickly, and can only do that with a loop.

while running:
    pass
# boucle presque inffinie, si il trouve un élément quit, le jeux s'arrête
# fundamental loop for using pygame
    #for event in pygame.event.get():
    # Loop over all captured events
        #if event.type == pygame.QUIT:
        # Test if pygame is ended
            #running = False
            #pygame.quit()
