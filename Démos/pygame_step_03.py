import pygame
from sys import exit
from typing import Tuple

WINDOW_SIZE: Tuple[int, int] = (480, 360)
WINDOW_TITLE: str = "pygame window 03"

# We use pygame colors dictionary !


class App:
# Make a class for the Application
# normally it's a Singleton (only 0 or 1 instance are allowed)
# but the subject of design patterns goes beyond this course
# https://refactoring.guru/design-patterns
    __window_size: Tuple[int, int] = WINDOW_SIZE
    __window_title: str = WINDOW_TITLE
    __screen: pygame.Surface = None
    __running: bool = False
    # Attrinuts

    def __init__(self) -> None:
        pygame.init()
        self.__init_screen()
        self.__running = True
    # Initialise 

    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(self.__window_size)
        pygame.display.set_caption(self.__window_title)
    # Initialise l'écran, définit fenêtre et titre

    def __handle_events(self, event) -> None:
        if event.type == pygame.QUIT:
            self.__running = False
            pygame.quit()
            exit()
        # Quitte si il reçoit la commande QUIT

    def execute(self) -> None:
        while self.__running:
            for event in pygame.event.get():
                self.__handle_events(event)
            pygame.draw.rect(self.__screen, pygame.color.THECOLORS["white"], (210, 160, 60, 40))
            pygame.display.flip()
        # Ou le joueur est et quel taille il a 
