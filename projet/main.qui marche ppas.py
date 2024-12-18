import pygame
from sys import exit
from typing import Tuple, List
from random import randint
from etres_vivants import EtreVivant, Plante, Animal, Lapin, Renard

WINDOW_SIZE: Tuple[int, int] = (400, 400)
WINDOW_TITLE: str = "simulation proie-prédateur"
FPS = 24



class App:
    __window_size: Tuple[int, int] = WINDOW_SIZE
    __window_title: str = WINDOW_TITLE
    __screen: pygame.Surface = None
    __running: bool = False

    __actor_position: pygame.Vector2
    __actor_speed: pygame.Vector2
    __actor_dimension: Tuple[int, int]
    __etreVivant_groupe : pygame.sprite.Group
    
    # Define an actor to be displayed

    def __init__(self) -> None:
        pygame.init()
        self.__init_screen()
        self.__init_actors()
        self.__running = True

    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(self.__window_size)
        pygame.display.set_caption(self.__window_title)

    def __init_actors(self) ->None:
        # Initialize an actor
        self.__actor_position: pygame.Vector2 = pygame.Vector2(210, 160)
        self.__actor_speed: pygame.Vector2 = pygame.Vector2((1, 1))
        self.__actor_dimension: Tuple[int, int] = (60, 40)
        self.__etreVivant_groupe = pygame.sprite.Group()
        for i in range(700):
            planteSprite = EtreVivantSprite(pygame.Surface((400,400)), "plante", self.__etreVivant_groupe)
        
        

    def __handle_events(self, event) -> None:
        if event.type == pygame.QUIT:
            self.__running = False
            pygame.quit()
            exit()

    def __update_actors(self) -> None:
    # Update actors (position, dimension, …)
        self.__actor_position += self.__actor_speed
        
        
    def __draw_screen(self)-> None :
        self.__screen.fill(pygame.color.THECOLORS["white"])

    def __draw_actors(self) -> None:
    # Draw actors on the screen
        pygame.draw.rect(self.__screen, pygame.color.THECOLORS["black"], (self.__actor_position, self.__actor_dimension))

    def execute(self) -> None:
        while self.__running:
            for event in pygame.event.get():
                self.__handle_events(event)
            self.__update_actors()
            self.__draw_screen()
            self.__draw_actors()
            pygame.display.flip()


class EtreVivantSprite(pygame.sprite.Sprite) :
    _etreVivant :  EtreVivant
    _type : str
    _surface : pygame.Surface
    _color : pygame.color = pygame.color
    _image : pygame.Surface
    _rect : pygame.Rect 
    _vitesse : pygame.Vector2
    _position : Tuple[int, int]
    
    #Reprendre classe actor + rajouter elements spécifiques
    def __init__(self, surface : pygame.Surface, type_name : str, *groups : List[pygame.sprite.Group]) -> None :
        pygame.sprite.Sprite.__init__(self, *groups)
        self._surface = surface
        
        self.rect = self._image.get_rect()
        self.rect.topleft = (random_x, random_y)
        self._set_image()
        self._set_rect()
        max_x = WINDOW_SIZE[0] - self.image.get_width()
        max_y = WINDOW_SIZE[1] - self.image.get_height()
        random_x = randint(0, max_x)
        random_y = randint(0, max_y)
        self._position = [random_x, random_y]
        self._set_type(type_name)
        
        if type_name == "plante" :
            self._surface = pygame.Vector2(210, 160)
            self._etreVivant =  Plante()
            self._vitesse = pygame.Vector2(0,0)
            self._color = pygame.color.THECOLORS["green"]
            
            
        
    @property
    def color(self) -> pygame.Color :
        self._color
    #Cette fonction donnne la couleur du sprite quand on lui demande
    
    def _set_color(self, color_name: str) -> None:
        if color_name not in pygame.color.THECOLORS.keys():
            raise ValueError("color must be in list of pygame.Color")
        self._color = pygame.Color(color_name)
        
    @property
    def _image(self) -> pygame.Surface:
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
    
#initialisation ou mise à jour du rectangle
    def _set_rect(self) -> None:
        rect = self.image.get_rect()
        rect.update(self._etreVivant.position, self._image.get_size())
        self._rect = rect
        
#verification des collisions avec les bords
    def test_touching_surface_boundaries(self) -> bool:
        # function to test boundaries
        # we only use relatives positions
        # so we don't have to use a lot of maths
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
    #Permet de ne pas sortir de l'écran
    
#méthode génerique de mise à jour 
    def update(self) -> None:
        pass
    


app = App()
app.execute()