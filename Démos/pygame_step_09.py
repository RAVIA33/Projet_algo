import pygame
from sys import exit
from random import randint
from typing import Tuple

WINDOW_SIZE: Tuple[int, int] = (400, 400)
WINDOW_TITLE: str = "pygame window 09"
FPS = 12


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
    #Plus de update et draw

#Les sprites : zone graphique qui se déplace sur l'écran
class ActorSprite(pygame.sprite.Sprite):
    _actor: Actor
    _color: pygame.Color
    _image: pygame.Surface  # pygame mandatory : it must be public to init the sprite
    _rect: pygame.Rect  # pygame mandatory : it must be public to init the sprite
                        #Attributs obligatoires quand on fait un sprite 

    def __init__(self, actor: Actor, color_name: str) -> None:
        pygame.sprite.Sprite.__init__(self) #initier class mère
        self._actor = actor
        self._set_color(color_name)
        self._set_image()
        self._set_rect()

    @property
    def color(self) -> pygame.Color:
        return self._color

    def _set_color(self, color_name: str) -> None:
        if color_name not in pygame.color.THECOLORS.keys():
            raise ValueError("color must be in list of pygame.Color")
        self._color = pygame.Color(color_name)
        #Si couleur non disponible, en donner une autre

    @property
    def image(self) -> pygame.Surface:
        return self._image

    def _set_image(self) -> None:
        image = pygame.Surface(self._actor.dimension)
        # set the pygame.Surface of the pygame.Sprite
        image.fill(pygame.Color("black"))
        image.set_colorkey(pygame.Color("black"))
        image.set_alpha(255) #Pixels noirs considérés comme invisibles 
        # the 3 lines above set the color black as "transparent"
        pygame.draw.rect(image, self.color, ((0, 0), image.get_size()))
        # draw a rectangle shape on the surface of the sprite
        self._image = image #setter de l'image

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    def _set_rect(self) -> None:
        rect = self.image.get_rect()
        rect.update(self._actor.position, self.image.get_size())
        self._rect = rect

    def update(self) -> None:
        pass


class ActorSpriteDrivenBySpeed(ActorSprite):
    def __init__(self, actor: Actor, color_name: str) -> None:
        super().__init__(actor, color_name)

    def update(self): 
        self._rect.move_ip(self._actor.speed)#move ip, déplace rectange selon vecteur speed
        self._actor.position = pygame.Vector2(self._rect.topleft) #nouvelle position du rectangle et la transforme en vecteur, envoi l'info au modèle


class App:
    __window_size: Tuple[int, int] = WINDOW_SIZE
    __window_title: str = WINDOW_TITLE
    __screen: pygame.Surface = None
    __running: bool = False
    __clock: pygame.time.Clock = pygame.time.Clock()
    __FPS: int = FPS

    __actors_sprites: pygame.sprite.Group
    # pygame handles sprites with sprite.Group instances
    # to group.update() and to group.draw() all sprites belonging to the group

    def __init__(self) -> None:
        pygame.init()
        self.__init_screen()
        self.__init_actors()
        self.__running = True

    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(self.__window_size)
        pygame.display.set_caption(self.__window_title)

    def __init_actors(self) -> None:
        random_speed: pygame.Vector2 = pygame.Vector2(randint(-1, 1), randint(-1, 1))
        actor: Actor = Actor(pygame.Vector2(210, 160), random_speed, (60, 40))
        self.__actors_sprites = pygame.sprite.Group()
        sprite: ActorSpriteDrivenBySpeed = ActorSpriteDrivenBySpeed(actor, "white")
        self.__actors_sprites.add(sprite)

    def __handle_events(self, event) -> None:
        if event.type == pygame.QUIT:
            self.__running = False
            pygame.quit()
            exit()

    def __update_actors(self) -> None:
        self.__actors_sprites.update()  #avant c'était une boucle. 

    def __draw_screen(self) -> None:
        self.__screen.fill(pygame.color.THECOLORS["black"])

    def __draw_actors(self) -> None:
        self.__actors_sprites.draw(self.__screen)

    def execute(self) -> None:
        while self.__running:
            self.__clock.tick(self.__FPS)
            for event in pygame.event.get():
                self.__handle_events(event)
            self.__update_actors()
            self.__draw_screen()
            self.__draw_actors()
            pygame.display.flip()
