import pygame
from sys import exit
from random import randint
from typing import List, Tuple

WINDOW_SIZE: Tuple[int, int] = (480, 360)
WINDOW_TITLE: str = "pygame window 07"
FPS: int = 12

#CREATION ACTEURS
class Actor:
    _position: pygame.Vector2
    _speed: pygame.Vector2
    _dimension: Tuple[int, int]

    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2, dimension: Tuple[int, int]) -> None:
        self._position = position
        self._speed = speed
        self._dimension = dimension

    @property
    def position(self) -> pygame.Vector2:
        return self._position

    @position.setter
    def position(self, position: pygame.Vector2) -> None:
        if position.x < 0 or position.y < 0:
            raise ValueError("each position values must be zero or positive")
        self._position = position
    #Getter et setter 
    @property
    def speed(self) -> pygame.Vector2:
        return self._speed

    @speed.setter
    def speed(self, speed: pygame.Vector2) -> None:
        self._speed = speed

    @property
    def dimension(self) -> Tuple[int, int]:
        return self._dimension

    @dimension.setter
    def dimension(self, dimension: Tuple[int, int]) -> None:
        if dimension[0] <= 0 or dimension[1] <= 0:
            raise ValueError("each dimension value must be positive")
        self._dimension = dimension

    def update(self) -> None:
        self._position = self._position + self._speed

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, pygame.color.THECOLORS["white"],(self._position, self._dimension))


class App:
    __window_size: Tuple[int, int] = WINDOW_SIZE
    __window_title: str = WINDOW_TITLE
    __screen: pygame.Surface = None
    __running: bool = False
    __clock: pygame.time.Clock = pygame.time.Clock()
    __FPS: int = FPS

    __actors: List[Actor] = []

    def __init__(self) -> None:
        pygame.init()
        self.__init_screen()
        self.__init_actors()
        self.__running = True

    def __init_screen(self) -> None:
        pygame.init()
        self.__screen = pygame.display.set_mode(self.__window_size)
        pygame.display.set_caption(self.__window_title)

    def __init_actors(self) -> None:
        random_speed: pygame.Vector2 = pygame.Vector2(randint(-1, 1), randint(-1, 1))
        actor: Actor = Actor(pygame.Vector2(210, 160), random_speed, (60, 40))
        self.__actors.append(actor)
        actor : Actor = Actor(pygame.Vector2(300,200), random_speed, (40, 40))
        self.__actors.append(actor)

    def __handle_events(self, event) -> None:
        if event.type == pygame.QUIT:
            self.__running = False
            pygame.quit()
            exit()

    def __update_actors(self) -> None:
        for actor in self.__actors:
            actor.update()

    def __draw_screen(self) -> None:
        self.__screen.fill(pygame.color.THECOLORS["black"])

    def __draw_actors(self) -> None:
        for actor in self.__actors:
            actor.draw(self.__screen)

    def execute(self) -> None:
        while self.__running:
            self.__clock.tick(self.__FPS)
            for event in pygame.event.get():
                self.__handle_events(event)
            self.__update_actors()
            self.__draw_screen()
            self.__draw_actors()
            pygame.display.flip()
