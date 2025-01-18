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
    type : EtreVivant
    _position: pygame.Vector2
    _speed: pygame.Vector2
    _dimension: Tuple[int, int]

    def __init__(self, type_name : str) -> None:
        self._position = pygame.Vector2(randint(0,400), randint(0,400))  #Car nimporte quel acteur à une position aléatoire sur l'écran
        if type_name == "plante" :
            self.type = Plante()
            self._dimension = [7,7]
            self._speed = pygame.Vector2(0,0)                     
            #car un acteur de type plante a une dimension [10,10] et une vitesse nulle
        elif type_name == "lapin":
            self.type = Lapin()
            self._dimension = [7, 7]
            self._speed = pygame.Vector2(randint(-1,1), randint(-1,1))
            #car un acteur de type lapin a une dimension [20,20] et se déplace aléatoirement de 0 à 1
        elif type_name == "renard" :
            self.type = Renard()
            self._dimension = [7,7]
            self._speed = pygame.Vector2(randint(-3,3), randint(-3,3))
            #car un acteur de type renard a une dimensions [30,30], et se déplace aléatoirement de 0 à 3
            

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
            if type(self._actor.type)  == Plante :
                self._actor._speed = pygame.Vector2(0,0)

            elif type(self._actor.type) == Lapin :
                self._actor._speed = pygame.Vector2(randint(-1,1), randint(-1,1))
                if self._actor._speed.length_squared() > 0:
                    self._actor.type.energie -= 1

                # self._actor.type.perdre_energie(1)
                # print(f"énergie lapin mnt:{self._actor.type.energie}")
                
            elif type(self._actor.type) == Renard :
                self._actor._speed = pygame.Vector2(randint(-3,3), randint(-3,3))
                if self._actor._speed.length_squared() > 0:
                    self._actor.type.energie -= 1
        if self._actor.type.energie <= 0:
            print(f"{self._actor.type.__class__.__name__} est mort par manque d'énergie")
            self.kill()  # Supprime le sprite s'il est mort
            return
        
                # self._actor.type.perdre_energie(2)
        # if self._actor.type.energie == 0:
        #     print("MORT")
        
            
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

         # Configuration des cycles et étapes
        self.__fps = FPS  #image par seconde
        self.__steps_per_cycle = 10  #nbr d'étapes par cycle
        self.__current_frame = 0  #compte les frames dans l'étape
        self.__current_step = 0  #compte les étapes dans le cycle
        self.__cycle = 1  #compte les cycles
        self.__plants_initial = 700  #nbr de plantes au début 

    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(self.__window_size)
        pygame.display.set_caption(self.__window_title)

    def __handle_events(self, event) -> None:
        if event.type == pygame.QUIT:
            self.__running = False
            pygame.quit()
            exit()

    def __init_actors(self) -> None:
        self.__actors_sprites = pygame.sprite.Group()# On crée un groupe pourles acteurs
        
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
            
    #méthode pour gérer les collisions entre les sprites
    def check_collision(self)-> None:
        MAX_LAPINS = 520  
        MAX_RENARDS = 22
        for sprite in self.__actors_sprites:  
            touch_sprites = pygame.sprite.spritecollide(sprite, self.__actors_sprites, False)
            
            for other_sprite in touch_sprites:
                if sprite == other_sprite:
                    continue  
            
                #vérifie si sprite est une instance de la class renard et si other_sprite est une instance de la class Lapin
                if isinstance(sprite._actor.type, Renard) and isinstance(other_sprite._actor.type, Lapin):  #si c'est le cas alors affiche "renard mange lapin"
                    if sprite._actor.type.energie >= sprite._actor.type.energie_maximale:
                        print(f"{sprite._actor.type.__class__.__name__} ne peut pas se nourrir, énergie maximale atteinte.")
                    else:
                        print("Renard mange un lapin")
                        energie_gagnee = other_sprite._actor.type.energie #le renard récupère toute l'énergie du lapin
                        sprite._actor.type.energie += energie_gagnee
                        other_sprite.kill()  #supprime le lapin
                        if sprite._actor.type.energie > sprite._actor.type.energie_maximale:
                            sprite._actor.type.energie = sprite._actor.type.energie_maximale
                    
                    # Vérification supplémentaire : si l'énergie devient négative par erreur, la limite à 0
                    if sprite._actor.type.energie < 0:
                        sprite._actor.type.energie = 0
                        print(f"{sprite._actor.type.__class__.__name__} est mort par manque d'énergie")
                        sprite.kill()  # Supprime le renard s'il n'a plus d'énergie  
                    
                    print(f"{sprite._actor.type.__class__.__name__} énergie actuelle : {sprite._actor.type.energie}")


                #vérifie si sprite est une instance de la class lapin et si other_sprite est une instance de la class plante
                elif isinstance(sprite._actor.type, Lapin) and isinstance(other_sprite._actor.type, Plante):
                    if sprite._actor.type.energie >= sprite._actor.type.energie_maximale:
                        print(f"{sprite._actor.type.__class__.__name__} ne peut pas se nourrir, énergie maximale atteinte.")
                    else:  
                        print("Lapin mange une plante")
                        energie_gagnee = other_sprite._actor.type.valeur_nutritive  #le lapin récup l'énergie de la plante
                        sprite._actor.type.energie += energie_gagnee
                        other_sprite.kill()  #supprime la plante
                        if sprite._actor.type.energie > sprite._actor.type.energie_maximale:
                            sprite._actor.type.energie = sprite._actor.type.energie_maximale

                    # Vérification supplémentaire : si l'énergie devient négative par erreur, la limite à 0
                    if sprite._actor.type.energie < 0:
                        sprite._actor.type.energie = 0
                        print(f"{sprite._actor.type.__class__.__name__} est mort par manque d'énergie")
                        sprite.kill()  # Supprime le lapin s'il n'a plus d'énergie

                    print(f"{sprite._actor.type.__class__.__name__} énergie actuelle : {sprite._actor.type.energie}")

                #reproduction
                elif type(sprite._actor.type) == type(other_sprite._actor.type) and isinstance(sprite._actor.type, Animal):
                    if isinstance(sprite._actor.type, Lapin):
                        max_population = MAX_LAPINS
                    elif isinstance(sprite._actor.type, Renard):
                        max_population = MAX_RENARDS
                    else:
                        continue

                    #vérification pop. max
                    current_population = sum(1 for s in self.__actors_sprites if isinstance(s._actor.type, type(sprite._actor.type))) #CHATGPT
                    if current_population >= max_population:
                        print(f"Population maximale de {type(sprite._actor.type).__name__.lower()} atteinte.")
                        continue

                    #crée les enfants
                    enfants = sprite._actor.type.se_reproduire()
                    for enfant in enfants:
                        color = "white" if isinstance(enfant, Lapin) else "orange"  # Détermine la couleur
                        ActorSprite(self.__screen, Actor(enfant.__class__.__name__.lower()), color, [self.__actors_sprites])
                        print(f"Un nouveau {enfant.__class__.__name__.lower()} est né avec {enfant.energie} d'énergie.")
                        
    def __update_actors(self) -> None:
        self.__actors_sprites.update()
        for sprite in self.__actors_sprites.copy():
            if not sprite._actor.type.est_vivant():  # Vérifie si l'entité est vivante
                sprite.kill()  # Supprime le sprite mort

    def afficher_resume_cycle(self) -> None:
        #affiche le récap des populations pour le cycle actuel
        nb_plantes = sum(1 for sprite in self.__actors_sprites if isinstance(sprite._actor.type, Plante))
        nb_lapins = sum(1 for sprite in self.__actors_sprites if isinstance(sprite._actor.type, Lapin))
        nb_renards = sum(1 for sprite in self.__actors_sprites if isinstance(sprite._actor.type, Renard))

        print(f"Cycle {self.__cycle}:")
        print(f"  Plantes: {nb_plantes}")
        print(f"  Lapins: {nb_lapins}")
        print(f"  Renards: {nb_renards}")

    def renouveler_plantes(self) -> None:
        nb_actuel = sum(1 for sprite in self.__actors_sprites if isinstance(sprite._actor.type, Plante))

        nb_a_ajouter = self.__plants_initial - nb_actuel

        #ajouter des nouvelles plantes
        for _ in range(nb_a_ajouter):
            plante = Actor("plante")
            ActorSprite(self.__screen, plante, "green", [self.__actors_sprites])

        #afficher ce message
        print(f"Renouvellement des plantes : {nb_a_ajouter} ajoutées (Total : {self.__plants_initial})")


    def __draw_screen(self) -> None:
        self.__screen.fill(pygame.color.THECOLORS["black"])

    def __draw_actors(self) -> None:
        self.__actors_sprites.draw(self.__screen)

    def execute(self) -> None:
        while self.__running:
            self.__clock.tick(self.__FPS)

            #gérer les événements
            for event in pygame.event.get():
                self.__handle_events(event)

            #met à jour les entités et collisions
            self.check_collision()    
            self.__update_actors()

            #gérer des frames et des cycles
            self.__current_frame += 1
            if self.__current_frame >= self.__FPS:  #étape dure 1 seconde 
                self.__current_frame = 0
                self.__current_step += 1  #on passe à létape suivante

                #vérification si le cycle est terminé
                if self.__current_step >= self.__steps_per_cycle:
                    self.afficher_resume_cycle()  #affiche le résumé des cycles 
                    self.renouveler_plantes()  #renouvelle les plantes
                    self.__cycle += 1  #passe au cycle suivant
                    self.__current_step = 0  #réinitialise les étapes

            #dessin de l'écran
            self.__draw_screen()
            self.__draw_actors()
            pygame.display.flip()

            
app = App()
app.execute()