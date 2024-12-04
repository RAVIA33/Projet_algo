import pygame
from sys import exit
# Needed to end cleanly App
# https://eng.libretexts.org/Bookshelves/Computer_Science/Programming_Languages/Making_Games_with_Python_and_Pygame_(Sweigart)/03%3A_Pygame_Basics/3.06%3A_The_QUIT_Event_and_pygame.quit()_Function#:~:text=Your%20programs%20should%20always%20call,()%20to%20terminate%20the%20program.
from typing import Dict, Tuple


WINDOW_SIZE: Tuple[int, int]  = (480, 360)
WINDOW_TITLE: str = "pygame window 02"
# Define pygame window title

colors: Dict = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "yellow": (255, 255, 0),
}
# In fact, pygame features a color dictionary ! en valeur RGB
# https://www.pygame.org/docs/ref/color_list.html

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
        pygame.draw.rect(screen, colors["white"], (210, 160, 60, 40))
        pygame.draw.circle(screen, colors["magenta"], (200, 200), 10,)
        pygame.draw.circle(screen, colors["blue"], (200, 100), 30, 4)
        # Dessine un rectangle blanc, avec coordonée coin haut gauche et largeur et hauteur, afficher sur screen
        # Draw a white rectangle of 60 x 40 pixels radius with the top left-hand corner at x = 210 and y = 160 inside the window screen
        # Coordinates are strictly positive and the origin position (x = 0, y = 0) is in the top left-hand corner
        # o 0 -> x right
        # 0
        # |
        # v
        # y
        # down
        pygame.display.flip()
        # must be call to update all display Surface
        # https://www.pygame.org/docs/ref/display.html#pygame.display.flip
