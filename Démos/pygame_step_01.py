import pygame
from sys import exit
# Needed to end cleanly App
# https://eng.libretexts.org/Bookshelves/Computer_Science/Programming_Languages/Making_Games_with_Python_and_Pygame_(Sweigart)/03%3A_Pygame_Basics/3.06%3A_The_QUIT_Event_and_pygame.quit()_Function#:~:text=Your%20programs%20should%20always%20call,()%20to%20terminate%20the%20program.
from typing import Dict, Tuple


WINDOW_SIZE: Tuple[int, int]  = (480, 360)
WINDOW_TITLE: str = "my first pygame window 01"
# Define pygame window title

def init_screen() -> pygame.Surface:
# cleaner way to init screen using a function
    screen: pygame.Surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)
    # set title to the window
    return screen

def handle_events(event) -> None:
# cleaner way to handle events using a function
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()
        # End and leave cleanly the App

def execute() -> None:
    pygame.init()
    screen = init_screen()
    running = True
    while running:
        for event in pygame.event.get():
            handle_events(event)
        pygame.display.flip() #raffraichi régulièrement la fenêtre
        # must be call to update all display Surface
        #Environnement d'exécution
        # https://www.pygame.org/docs/ref/display.html#pygame.display.flip
