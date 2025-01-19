import pygame
from random import randint
from sys import exit
from typing import List, Tuple
from random import randint
from etres_vivants import *
from parametres import *
from sprite import *






        
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

         #configuration des cycles et étapes
        self.__FPS = FPS  #image par seconde
        self.__steps_per_cycle = 12  #nbr d'étapes par cycle
        self.__current_frame = 0  #compte les frames dans l'étape
        self.__current_step = 1  #compte les étapes dans le cycle
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
        self.__actors_sprites = pygame.sprite.Group()
        self.create_actors(plante_type_name, plante_nombre_initial, plante_couleur)
        self.create_actors(lapin_type_name, lapin_nombre_initial, lapin_couleur)
        self.create_actors(renard_type_name, renard_nombre_initial, renard_couleur)
                           
    def create_actors(self, type_name: str, count: int, color: str) -> None:
       #gérer la création des entité
        for _ in range(count):
            actor = Actor(type_name)  # Crée un acteur (plante, lapin, ou renard)
            ActorSprite(self.__screen, actor, color, [self.__actors_sprites])  # Associe un sprite


    def __update_actors(self) -> None:
        self.__actors_sprites.update()
        for sprite in self.__actors_sprites.copy():
            if not sprite._actor.type.est_vivant():  
                sprite.kill()  
                        
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
                    #if sprite._actor.type.energie >= sprite._actor.type.energie_maximale:
                        #print(f"{sprite._actor.type.__class__.__name__} ne peut pas se nourrir, énergie maximale atteinte.")
                    if sprite._actor.type.energie < sprite._actor.type.energie_maximale:
                        #print("Renard mange un lapin")
                        energie_gagnee = other_sprite._actor.type.energie #le renard récupère toute l'énergie du lapin
                        sprite._actor.type.energie += energie_gagnee
                        other_sprite.kill()  #supprime le lapin
                        if sprite._actor.type.energie > sprite._actor.type.energie_maximale:
                            sprite._actor.type.energie = sprite._actor.type.energie_maximale
                    
                    #vérification supplémentaire : si l'énergie devient négative par erreur, la limite à 0
                    if sprite._actor.type.energie < 0:
                        sprite._actor.type.energie = 0
                        #print(f"{sprite._actor.type.__class__.__name__} est mort par manque d'énergie")
                        sprite.kill()  #supprime le renard s'il n'a plus d'énergie  
                    
                    #print(f"{sprite._actor.type.__class__.__name__} énergie actuelle : {sprite._actor.type.energie}")


                #vérifie si sprite est une instance de la class lapin et si other_sprite est une instance de la class plante
                elif isinstance(sprite._actor.type, Lapin) and isinstance(other_sprite._actor.type, Plante):
                    #if sprite._actor.type.energie >= sprite._actor.type.energie_maximale:
                        #print(f"{sprite._actor.type.__class__.__name__} ne peut pas se nourrir, énergie maximale atteinte.")
                    if sprite._actor.type.energie < sprite._actor.type.energie_maximale:
                        #print("Lapin mange une plante")
                        energie_gagnee = other_sprite._actor.type.valeur_nutritive  #le lapin récup l'énergie de la plante
                        sprite._actor.type.energie += energie_gagnee
                        other_sprite.kill()  #supprime la plante
                        if sprite._actor.type.energie > sprite._actor.type.energie_maximale:
                            sprite._actor.type.energie = sprite._actor.type.energie_maximale

                    #vérification supplémentaire : si l'énergie devient négative par erreur, la limite à 0
                    if sprite._actor.type.energie < 0:
                        sprite._actor.type.energie = 0
                        #print(f"{sprite._actor.type.__class__.__name__} est mort par manque d'énergie")
                        sprite.kill()  #supprime le lapin s'il n'a plus d'énergie

                    #print(f"{sprite._actor.type.__class__.__name__} énergie actuelle : {sprite._actor.type.energie}")

                #reproduction
                elif type(sprite._actor.type) == type(other_sprite._actor.type) and isinstance(sprite._actor.type, Animal):
                    max_population = MAX_LAPINS if isinstance(sprite._actor.type, Lapin) else MAX_RENARDS

                    #vérification pop. max
                    current_population = sum(1 for s in self.__actors_sprites if isinstance(s._actor.type, type(sprite._actor.type))) #CHATGPT
                    if current_population >= max_population:
                        #print(f"Population maximale de {type(sprite._actor.type).__name__.lower()} atteinte.")
                        continue

                    #crée les enfants
                    enfants = sprite._actor.type.se_reproduire()
                    for enfant in enfants:
                        if current_population >= max_population:
                            break  #stop la reproduction si le max est atteint 
                        current_population += 1
                        color = "white" if isinstance(enfant, Lapin) else "orange"  
                        ActorSprite(self.__screen, Actor(enfant.__class__.__name__.lower()), color, [self.__actors_sprites])#CHATGPT
                        #print(f"Un nouveau {enfant.__class__.__name__.lower()} est né avec {enfant.energie} d'énergie.")
                        


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
        self.afficher_resume_cycle()
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
                print(self.__cycle, self.__current_step)
                self.__current_step += 1  #on passe à létape suivante

                #vérification si le cycle est terminé
                if self.__current_step > self.__steps_per_cycle: 
                    self.__cycle += 1 #passe au cycle suivant
                    self.afficher_resume_cycle()  #affiche le résumé des cycles 
                    self.renouveler_plantes()  #renouvelle les plantes 
                    self.__current_step = 1  #réinitialise les étapes

            #dessin de l'écran
            self.__draw_screen()
            self.__draw_actors()
            pygame.display.flip()

            
app = App()
app.execute()