import pygame
from random import randint
from sys import exit
from typing import List, Tuple
from random import randint
from etres_vivants import *
from parametres import *

class Actor:
    # type : EtreVivant
    # _position: pygame.Vector2
    # _speed: pygame.Vector2
    # _dimension: Tuple[int, int]

    def __init__(self, type_name : str) -> None:
        self._position = pygame.Vector2(randint(0,WINDOW_SIZE[0]), randint(0,WINDOW_SIZE[1]))  #Car nimporte quel acteur à une position aléatoire sur l'écran qui est WINDOW_SIZE
        if type_name == plante_type_name :
            self.type = Plante()
            self._dimension = plante_dimension
            self._speed = pygame.Vector2(0,0)                     
            #car un acteur de type plante a une dimension [5,5] et une vitesse nulle
        elif type_name == lapin_type_name:
            self.type = Lapin()
            self._dimension = lapin_dimension
            self._speed = pygame.Vector2(randint(*lapin_vitesse), randint(*lapin_vitesse))
            #car un acteur de type lapin a une dimension [7,7] et se déplace aléatoirement de 0 à 1
        elif type_name == renard_type_name :
            self.type = Renard()
            self._dimension = renard_dimension
            self._speed = pygame.Vector2(randint(*renard_vitesse), randint(*renard_vitesse))
            #car un acteur de type renard a une dimensions [10,10], et se déplace aléatoirement de 0 à 3
            

    @property
    def position(self) -> pygame.Vector2:
        return self._position

    @position.setter
    def position(self, position: pygame.Vector2) -> None:
        if position.x < 0 or position.y < 0:
            raise ValueError("chaque valeur doit être nulle ou positive.")
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
            raise ValueError("chaque dimension doit être positive.")
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
        #vérifier les collisions avec les bords 
        if self.rect.left < 0:
            self.rect.left = 0  #remettre bord gauche
            self._actor.speed.x = -self._actor.speed.x  #inverser la direction 
        if self.rect.right > self._surface.get_width():
            self.rect.right = self._surface.get_width()  #remettre au bord droit
            self._actor.speed.x = -self._actor.speed.x  #inverser la direction horizontale
        if self.rect.top < 0:
            self.rect.top = 0  #remettre au bord supérieur
            self._actor.speed.y = -self._actor.speed.y  #inverser la direction verticale
        if self.rect.bottom > self._surface.get_height():
            self.rect.bottom = self._surface.get_height()  #remettre au bord inférieur
            self._actor.speed.y = -self._actor.speed.y
    
 
    def update(self):
        if self._tick_number % 24 == 0 :
            if type(self._actor.type)  == Plante :
                self._actor._speed = pygame.Vector2(0,0)

            elif type(self._actor.type) == Lapin :
                self._actor._speed = pygame.Vector2(randint(-1,1), randint(-1,1))
                if self._actor._speed.length_squared() > 0:
                    self._actor.type.energie -= 5
                
                # Vérifie si le lapin a atteint son âge maximal en cycles
                
                if self._actor.type.age >= self._actor.type.age_maximal * 12 * 24:  # 3 cycles = 3 fois 24 étapes pour le lapin
                    #print("Le lapin est mort après", self._actor.type.age_maximal, "cycles")
                    self._actor.type.vivant = False  # Le lapin meurt
                    self.kill()  # Supprime le sprite du lapin
                    return

                # self._actor.type.perdre_energie(1)
                # print(f"énergie lapin mnt:{self._actor.type.energie}")
                
            elif type(self._actor.type) == Renard :
                self._actor._speed = pygame.Vector2(randint(-3,3), randint(-3,3))
                if self._actor._speed.length_squared() > 0:
                    self._actor.type.energie -= 0.5
                
                # Vérifie si le renard a atteint son âge maximal en cycles
                if self._actor.type.age >= self._actor.type.age_maximal * 12 * 24:  # 5 cycles = 5 fois 24 étapes pour le renard
                    print("Le renard est mort après", self._actor.type.age_maximal, "cycles")
                    self._actor.type.vivant = False  # Le renard meurt
                    self.kill()  # Supprime le sprite du renard
                    return
        if self._actor.type.energie <= 0:
            #print(f"{self._actor.type.__class__.__name__} est mort par manque d'énergie")
            self.kill()  # Supprime le sprite s'il est mort
            return
        
                # self._actor.type.perdre_energie(2)
        # if self._actor.type.energie == 0:
        #     print("MORT")
        
            
        self.rect.move_ip(self._actor._speed)
        if not self.test_touching_surface_boundaries():
            self._actor.position = pygame.Vector2(self.rect.topleft)
        self._tick_number += 1
        
        self._actor.type.vieillir()