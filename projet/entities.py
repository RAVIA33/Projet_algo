from typing import Tuple

class EtreVivant  : 
    #Attributs communs à tous les êtres vivants
    energie : int                   #Energie actuelle de l'entité
    energie_maximale : int          
    position : Tuple[int, int]
    age_maximal : int               # Durée de vie 
    age : int                       #Âge actuel
    vivant : bool                   #Indique si l'être est vivant ou non
    
    def __init__(self, energie_initiale : int, energie_maximale : int, age_maximale:int, vivant : bool ) :
        self.energie = energie_initiale
        self.energie_maximale = energie_maximale
        self.age = 0
        self.age_maximale = age_maximale
        self.position = (0,0) #position par défaut pour le moment 
        self.vivant = True
        
    #Quand l'énergie baisse, on vérifie que l'entité est toujours vivante
    def perdre_energie(self, quantite) :
        self.energie -= quantite
        if self.energie <= 0 :
        self.vivant = False   #self souligné en rouge, peut etre ajouter un getter @
    
    def vieillir(self) :
        self.age += 1
        if self.age > self.age_maximal :
            self.vivant = False 


#Paramètres de départ pour les plantes
plante_quantite_initial = 700
plante_energie_initiale = 3
plante_energie_fournie = 3

class Plante(EtreVivant) :
    valeur_nutritive : int
    
    def __init__(self) :
        super().__init__(energie_initiale = 3, energie_maximale = 3, age_maximal = float("inf"))
            #float "inf" (Chatgpt) - les plantes ne meurent pas donc leur âge maximal est infini
        self.valeur_nutritive = 3
    
    
    def se_faire_manger(self) :
        self.vivant = False 
        #Est-ce qu'on ajoute le fait de fournir de l'énergie ?
        
        
class Animal(EtreVivant) :
    reproduction : Tuple[int,int]
    vitesse : int
    
    def __init__(self, energie_initiale : int, energie_maximale : int, age_maximal : int, reproduction : Tuple[int, int]) :
        super().__init__(energie_initiale, energie_maximale, age_maximal)
        self.reproduction = reproduction
            
    #def se_reproduire(self) -> int : 
        #A définir : nombre aleatoire allant d'un int à un int, définit dans "reproduction"
        
    def se_deplacer(self, environnement):
        #A définir plus tard


#Class Lapin paramètres initiaux:
lapin_nombre_initial = 520
lapin_energie_initiale = 10
lapin_energie_maximale = 20
lapin_vitesse = 1
lapin_age_maximal = 5
lapin_reproduction_max = 3
lapin_reproduction_min = 1
lapin_energie_fournie = 16

class Lapin(Animal):
    valeur_nutritive : int
    def __init__(self):
        super().__init__(energie_initiale=10, energie_maximale=20, vitesse=1, age_maximal=5, reproduction=(1, 3))
        self.valeur_nutritive = 16
        
        
#Class Renard, paramètres initiaux :
renard_nombre_initial = 22
renard_energie_initiale = 25
renard_energie_maximale = 50
renard_vitesse = 2
renard_age_maximal = 3
renard_reproduction_max = 5
renard_reproduction_min = 1

class Renard(Animal) :
    def __init__(self):
        super().__init__(energie_initiale=25, energie_maximale= 50, vitesse = 2, age_maximal=3, reproduction = (1,5))
        
#comment on fait pour optenir un diagramme déja ?


    
    








    


    