import pygame
from random import randint
from sys import exit
from typing import List, Tuple
from random import randint
from etres_vivants import EtreVivant, Plante, Animal, Lapin, Renard


WINDOW_SIZE: Tuple[int, int] = (400, 400)
WINDOW_TITLE: str = "pygame window 12"
FPS = 24


class Actor:
    _type : EtreVivant
    _position: pygame.Vector2
    _speed: pygame.Vector2
    _dimension: Tuple[int, int]

    def __init__(self, type_name : str) -> None:
        self._position = pygame.Vector2(randint(0,400), randint(0,400))  #Car nimporte quel acteur à une position aléatoire sur l'écran
        if type_name == "plante" :
            self._type = Plante()
            self._dimension = [7,7]
            self._speed = pygame.Vector2(0,0)                     
            #car un acteur de type plante a une dimension [10,10] et une vitesse nulle
        elif type_name == "lapin":
            self._type = Lapin()
            self._dimension = [7, 7]
            self._speed = pygame.Vector2(randint(-1,1), randint(-1,1))
            #car un acteur de type lapin a une dimension [20,20] et se déplace aléatoirement de 1
        elif type_name == "renard" :
            self._type = Renard()
            self._dimension = [7,7]
            self._speed = pygame.Vector2(randint(-3,3), randint(-3,3))
            #car un acteur de type renard a une dimensions [30,30], et se déplace aléatoirement de 3
            

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


class ActorSprite(pygame.sprite.Sprite):
    _surface: pygame.Surface
    # added to get information about the surface where sprite move to test boundaries
    _actor: Actor
    _color: pygame.Color
    _image: pygame.Surface
    _rect: pygame.Rect
    _tick_number = int

    def __init__(self, surface: pygame.Surface, actor: Actor, color_name: str, *groups: List[pygame.sprite.Group]) -> None:
        pygame.sprite.Sprite.__init__(self, *groups)
        self._surface = surface
        self._actor = actor
        self._tick_number = 0
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

    @property
    def image(self) -> pygame.Surface:
        return self._image

    def _set_image(self) -> None:
        image: pygame.Surface = pygame.Surface(self._actor.dimension)
        image.fill(pygame.Color("black"))
        image.set_colorkey(pygame.Color("black"))
        image.set_alpha(255)
        pygame.draw.rect(image, self.color, ((0, 0), image.get_size()), 5)
        self._image = image

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    def _set_rect(self) -> None:
        rect = self.image.get_rect()
        rect.update(self._actor.position, self.image.get_size())
        self._rect = rect

    def test_touching_surface_boundaries(self) -> None:
        # Vérifier les collisions avec les bords et inverser la direction si nécessaire
        if self.rect.left < 0:
            self.rect.left = 0  # Positionner au bord gauche
            self._actor.speed.x = -self._actor.speed.x  # Inverser la direction horizontale
        if self.rect.right > self._surface.get_width():
            self.rect.right = self._surface.get_width()  # Positionner au bord droit
            self._actor.speed.x = -self._actor.speed.x  # Inverser la direction horizontale
        if self.rect.top < 0:
            self.rect.top = 0  # Positionner au bord supérieur
            self._actor.speed.y = -self._actor.speed.y  # Inverser la direction verticale
        if self.rect.bottom > self._surface.get_height():
            self.rect.bottom = self._surface.get_height()  # Positionner au bord inférieur
            self._actor.speed.y = -self._actor.speed.y
    
    def update(self):
        if self._tick_number % 10 == 0 :
            if type(self._actor._type)  == Plante :
                self._actor._speed = pygame.Vector2(0,0)
            elif type(self._actor._type) == Lapin :
                self._actor._speed = pygame.Vector2(randint(-1,1), randint(-1,1))
            elif type(self._actor._type) == Renard :
                self._actor._speed = pygame.Vector2(randint(-3,3), randint(-3,3))
            
        self.rect.move_ip(self._actor._speed)
        if not self.test_touching_surface_boundaries():
            self._actor.position = pygame.Vector2(self.rect.topleft)
        self._tick_number += 1
    
class App:
    __window_size: Tuple[int, int] = WINDOW_SIZE
    __window_title: str = WINDOW_TITLE
    __screen: pygame.Surface = None
    __running: bool = False
    __clock: pygame.time.Clock = pygame.time.Clock()
    __FPS: int = FPS
    __actors_sprites: pygame.sprite.Group

    def __init__(self) -> None:
        pygame.init()
        self.__init_screen()
        self.__init_actors()
        self.__running = True

    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(self.__window_size)
        pygame.display.set_caption(self.__window_title)

    def __handle_events(self, event) -> None:
        if event.type == pygame.QUIT:
            self.__running = False
            pygame.quit()
            exit()

    def __init_actors(self) -> None:
        self.__actors_sprites = pygame.sprite.Group()       # On crée un groupe pourles acteurs
        
        #Création des plantes
        for _ in range(700):
            plante = Actor("plante")                            
            ActorSprite(self.__screen, plante, "green", [self.__actors_sprites])

        #Création des lapins
        for _ in range(520) :
            lapin = Actor("lapin") 
            ActorSprite(self.__screen, lapin, "white", [self.__actors_sprites])
        
        #Création des renards
        for _ in range(22):
            renard = Actor("renard")
            ActorSprite(self.__screen, renard, "orange", [self.__actors_sprites])
            
            
             

    def __update_actors(self) -> None:
        self.__actors_sprites.update()

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
            
app = App()
app.execute()