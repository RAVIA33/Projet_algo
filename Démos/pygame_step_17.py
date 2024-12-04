from abc import ABC
import pygame
from random import randint
from sys import exit
from typing import List, Tuple

WINDOW_SIZE: Tuple[int, int] = (480, 360)
WINDOW_TITLE: str = "pygame window 17"
FPS: int = 24


class Actor:
    _position: pygame.Vector2
    _speed: pygame.Vector2

    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2) -> None:
        self._position = position
        self._speed = speed

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


class SpriteShapeFactory(ABC):
    @classmethod
    def create_sprite_shape(cls, shape_name: str, dimension: Tuple[int, int] | int, color_name: str, border_width: int = 0, inner_color_name: str = "black") -> "SpriteShape":
        match shape_name:
            case "rectangle":
                return SpriteShapeRectangle(dimension, color_name, border_width, inner_color_name)
            case "circle":
                return SpriteShapeCircle(dimension, color_name, border_width, inner_color_name)
            case _:
                raise ValueError("Invalid shape")


class SpriteShape:
    _dimension: Tuple[int, int] | int
    _color: pygame.Color
    _border_width: int
    _inner_color: pygame.Color
    _shape_name: str

    def __init__(self, dimension: Tuple[int, int] | int, color_name: str, border_width: int = 5, inner_color_name: str = "black") -> None:
        self._dimension = dimension
        self._border_width = border_width
        self._color = self._set_color(color_name)
        self._border_width = border_width
        self._inner_color = self._set_color(inner_color_name)

    @property
    def dimension(self) -> Tuple[int, int] | int:
        return self._dimension

    @property
    def border_width(self) -> int:
        return self._border_width

    @border_width.setter
    def border_width(self, border_width) -> None:
        if border_width < 0:
            raise ValueError("border_width must be positive")
        self._border_width = border_width

    @property
    def color(self) -> pygame.Color:
        return self._color

    @property
    def inner_color(self) -> pygame.Color:
        return self._inner_color

    def _set_color(self, color_name: str) -> pygame.Color:
        if color_name not in pygame.color.THECOLORS.keys():
            raise ValueError("color must be in list of pygame.Color")
        return pygame.Color(color_name)

    def set_shape(self, image: pygame.Surface) -> None:
        pass


class SpriteShapeRectangle(SpriteShape):
    _dimension: Tuple[int, int]

    def __init__(self, dimension: Tuple[int, int], color_name: str, border_width: int = 5, inner_color_name: str = "black") -> None:
        super().__init__(dimension, color_name, border_width, inner_color_name)
        self._dimension = dimension

    @property
    def dimension(self) -> Tuple[int, int]:
        return self._dimension

    @dimension.setter
    def dimension(self, dimension: Tuple[int, int]) -> None:
        if dimension[0] <= 0 or dimension[1] <= 0:
            raise ValueError("dimension values must be positives")
        self._dimension = dimension

    def set_shape(self, image: pygame.Surface) -> None:
        if self._border_width != 0:
            pygame.draw.rect(image, self.inner_color, ((0, 0), self.dimension), 0)
        pygame.draw.rect(image, self.color, ((0, 0), self.dimension), self.border_width)


class SpriteShapeCircle(SpriteShape):
    _dimension: int

    def __init__(self, dimension: int, color_name: str, border_width: int = 5, inner_color_name: str = "black") -> None:
        super().__init__(dimension, color_name, border_width, inner_color_name)
        self._dimension = dimension

    @property
    def dimension(self) -> int:
        return self._dimension

    @dimension.setter
    def dimension(self, dimension: int) -> None:
        if dimension <= 0:
            raise ValueError("dimension value must be positive")
        self._dimension = dimension

    def set_shape(self, image: pygame.Surface) -> None:
        radius = self.dimension / 2
        if self._border_width != 0:
            pygame.draw.circle(image, self.inner_color, image.get_rect().center, radius, 0)
        pygame.draw.circle(image, self.color, image.get_rect().center, radius, self.border_width)


class ActorSprite(pygame.sprite.Sprite):
    _surface: pygame.Surface
    _actor: Actor
    _sprite_shape: SpriteShape
    _image: pygame.Surface
    _rect: pygame.Rect

    def __init__(self, surface: pygame.Surface, actor: Actor, sprite_shape: SpriteShape, *groups: List[pygame.sprite.Group]) -> None:
        pygame.sprite.Sprite.__init__(self, *groups)
        self._surface = surface
        self._actor = actor
        self._sprite_shape = sprite_shape
        self._set_image()
        self._set_rect()

    @property
    def image(self) -> pygame.Surface:
        return self._image

    def _set_image(self) -> None:
        if type(self._sprite_shape.dimension) is int:
            image: pygame.Surface = pygame.Surface((self._sprite_shape.dimension, self._sprite_shape.dimension))
        else:
            image:pygame.Surface = pygame.Surface(self._sprite_shape.dimension)
        image.fill(pygame.Color("black"))
        image.set_colorkey(pygame.Color("black"))
        image.set_alpha(255)
        self._sprite_shape.set_shape(image)
        self._image = image

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    def _set_rect(self) -> None:
        rect = self.image.get_rect()
        rect.update(self._actor.position, self.image.get_size())
        self._rect = rect

    def test_touching_surface_boundaries(self) -> bool:
        touch_boundaries = False
        if not self._surface.get_rect().collidepoint(self.rect.topleft):
            touch_boundaries = True
        if self.rect.left < 0:
            self.rect.move_ip(1, 0)
        if self.rect.right > self._surface.get_width():
            self.rect.move_ip(-1, 0)
        if self.rect.top < 0:
            self.rect.move_ip(0, 1)
        if self.rect.bottom > self._surface.get_height():
            self.rect.move_ip(0, -1)
        return touch_boundaries

    def update(self) -> None:
        pass

    def __del__(self):
        del self._actor


class ActorSpriteDrivenByMouse(ActorSprite):
    def __init__(self, surface: pygame.Surface, actor: Actor, sprite_shape: SpriteShape, *groups: List[pygame.sprite.Group]) -> None:
        super().__init__(surface, actor, sprite_shape, *groups)

    def update(self):
        if pygame.mouse.get_focused():
            self._rect.topleft = pygame.mouse.get_pos()
            self._rect.move_ip(1, 1)
            if not self.test_touching_surface_boundaries():
                self._actor.position = pygame.Vector2(self.rect.topleft)


class ActorSpriteDrivenByRandom(ActorSprite):
    def __init__(self, surface: pygame.Surface, actor: Actor, sprite_shape: SpriteShape, *groups: List[pygame.sprite.Group]) -> None:
        super().__init__(surface, actor, sprite_shape, *groups)

    def update(self):
        random_speed: pygame.Vector2 = pygame.Vector2(randint(-1, 1), randint(-1, 1))
        self._rect.move_ip(random_speed)
        if not self.test_touching_surface_boundaries():
            self._actor.position = pygame.Vector2(self.rect.topleft)


class ActorSpriteDrivenBySpeed(ActorSprite):
    def __init__(self, surface: pygame.Surface, actor: Actor, sprite_shape: SpriteShape, *groups: List[pygame.sprite.Group]) -> None:
        super().__init__(surface, actor, sprite_shape, *groups)

    def update(self):
        self.rect.move_ip(self._actor.speed)
        if not self.test_touching_surface_boundaries():
            self._actor.position = pygame.Vector2(self.rect.topleft)


class App:
    __window_size: Tuple[int, int] = WINDOW_SIZE
    __window_title: str = WINDOW_TITLE
    __screen: pygame.Surface = None
    __running: bool = False
    __clock: pygame.time.Clock = pygame.time.Clock()
    __FPS: int = FPS

    __player_sprite: pygame.sprite.Group
    __actor_driven: Actor
    __actor_driven_sprite: pygame.sprite.Group
    __actors_sprites: pygame.sprite.Group
    __actors_random_sprites: pygame.sprite.Group

    __number_of_actors_sprites: int = 3
    __kill_actors_sprites: bool

    def __init__(self) -> None:
        pygame.init()
        self.__kill_actors_sprites = True
        self.__init_screen()
        self.__init_actors()
        self.__running = True

    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(self.__window_size)
        pygame.display.set_caption(self.__window_title)

    def __init_actors(self) -> None:
        self.__player_sprite = pygame.sprite.Group()
        player: Actor = Actor(pygame.Vector2(0, 0), pygame.Vector2(1, 1))
        player_sprite_shape = SpriteShapeFactory.create_sprite_shape("circle", 60, "white", 0, "grey")
        ActorSpriteDrivenByMouse(self.__screen, player, player_sprite_shape, [self.__player_sprite])

        self.__actor_driven_sprite = pygame.sprite.Group()
        self.__actor_driven = Actor(pygame.Vector2(210, 160), pygame.Vector2(0, 0))
        actor_driven_sprite_shape = SpriteShapeFactory.create_sprite_shape("rectangle", (40, 60), "green", 10, "white")
        ActorSpriteDrivenBySpeed(self.__screen, self.__actor_driven, actor_driven_sprite_shape, [self.__actor_driven_sprite])

        self.__actors_sprites = pygame.sprite.Group()
        for _ in range(self.__number_of_actors_sprites):
            random_position: pygame.Vector2 = pygame.Vector2(randint(0, 420), randint(0, 320))
            random_speed: pygame.Vector2 = pygame.Vector2(randint(-1, 1), randint(-1, 1))
            actor: Actor = Actor(random_position, random_speed)
            actor_sprite_shape = SpriteShapeFactory.create_sprite_shape("rectangle", (40, 40), "blue", 5, "black")
            ActorSpriteDrivenBySpeed(self.__screen, actor, actor_sprite_shape, [self.__actors_sprites])

        self.__actors_random_sprites = pygame.sprite.Group()
        actor_01: Actor = Actor(pygame.Vector2(210, 160), pygame.Vector2(1, 1))
        actor_01_sprite_shape = SpriteShapeFactory.create_sprite_shape("rectangle", (60, 40), "red", 5, "grey")
        ActorSpriteDrivenByRandom(self.__screen, actor_01, actor_01_sprite_shape, [self.__actors_random_sprites])

    def __handle_events(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.__actor_driven.speed = (1, 0)
            if event.key == pygame.K_LEFT:
                self.__actor_driven.speed = (-1, 0)
            if event.key == pygame.K_UP:
                self.__actor_driven.speed = (0, -1)
            if event.key == pygame.K_DOWN:
                self.__actor_driven.speed = (0, 1)
        elif event.type == pygame.QUIT:
            self.__running = False
            pygame.quit()
            exit()

    def __update_actors(self) -> None:
        self.__player_sprite.update()
        self.__actor_driven_sprite.update()
        self.__actors_sprites.update()
        self.__actors_random_sprites.update()
        for sprite_player in self.__player_sprite.sprites():
            actors_hit_list = pygame.sprite.spritecollide(sprite_player, self.__actors_sprites, self.__kill_actors_sprites)
            if len(actors_hit_list) != 0:
                print("Catch one of them !")

    def __draw_screen(self) -> None:
        self.__screen.fill(pygame.color.THECOLORS["black"])

    def __draw_actors(self) -> None:
        # The order is important because elements are drawn layer by layer
        self.__actors_random_sprites.draw(self.__screen)
        self.__actor_driven_sprite.draw(self.__screen)
        self.__actors_sprites.draw(self.__screen)
        self.__player_sprite.draw(self.__screen)

    def execute(self) -> None:
        while self.__running:
            self.__clock.tick(self.__FPS)
            for event in pygame.event.get():
                self.__handle_events(event)
            self.__update_actors()
            self.__draw_screen()
            self.__draw_actors()
            pygame.display.flip()
