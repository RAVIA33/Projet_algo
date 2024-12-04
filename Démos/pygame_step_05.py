import pygame
from random import randint
from sys import exit
from typing import Tuple

WINDOW_SIZE: Tuple[int, int] = (480, 360)
WINDOW_TITLE: str = "pygame window 05"


class App:
    __window_size: Tuple[int, int] = WINDOW_SIZE
    __window_title: str = WINDOW_TITLE
    __screen: pygame.Surface = None
    __running: bool = False

    __actor_position: pygame.Vector2
    __actor_speed: pygame.Vector2
    __actor_dimension: Tuple[int, int]

    def __init__(self) -> None:
        pygame.init()
        self.__init_screen()
        self.__init_actors()
        self.__running = True

    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(self.__window_size)
        pygame.display.set_caption(self.__window_title)

    def __init_actors(self) ->None:
        self.__actor_position: pygame.Vector2 = pygame.Vector2(210, 160)
        self.__actor_speed: pygame.Vector2 = pygame.Vector2(randint(-1, 1), randint(-1, 1))
        self.__actor_dimension: Tuple[int, int] = (60, 40)

    def __handle_events(self, event) -> None:
        if event.type == pygame.QUIT:
            self.__running = False
            pygame.quit()
            exit()

    def __update_actors(self) -> None:
        self.__actor_position = self.__actor_position + self.__actor_speed

    def __draw_screen(self) -> None:
    # draw the background screen, here it's simply all in black
        self.__screen.fill(pygame.color.THECOLORS["black"])

    def __draw_actors(self) -> None:
        pygame.draw.rect(self.__screen, pygame.color.THECOLORS["white"], (self.__actor_position, self.__actor_dimension))

    def execute(self) -> None:
        while self.__running:
            for event in pygame.event.get():
                self.__handle_events(event)
            self.__update_actors()
            self.__draw_screen()
            self.__draw_actors()
            pygame.display.flip()
