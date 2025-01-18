from typing import Tuple
from typing import List
import random

class EtreVivant  : 
    #Attributs communs à tous les êtres vivants
    energie: int                   #Energie actuelle de l'entité
    energie_maximale : int          
    age_maximal : int               # Durée de vie 
    age : int                       #Âge actuel
    vivant : bool                   #Indique si l'être est vivant ou non
    
    def __init__(self,  energie_initiale : int, energie_maximale : int, age_maximal:float) :
        self.energie = energie_initiale
        self.energie_maximale = energie_maximale
        self.age = 0
        self.age_maximal = age_maximal
        self.vivant = True
        
    #Quand l'énergie baisse, on vérifie que l'entité est toujours vivante
    def perdre_energie(self, quantite) :
        self.energie -= quantite
        if self.energie <= 0:
            self.energie = 0
            self.vivant = False #la condition false pour que si son énergie arrive à zéro ça le supprime 
    
    def vieillir(self) :
        self.age += 1
        if self.age > self.age_maximal : # > ou >= pour l'age ou il meurt ?
            self.vivant = False 
    def est_vivant(self) -> bool:
        return self.energie > 0

class Plante(EtreVivant) :
    valeur_nutritive : int 
    
    def __init__(self) :
        super().__init__(energie_initiale = 3, energie_maximale = 3, age_maximal = float("inf"))
            #float "inf" (Chatgpt) - les plantes ne meurent pas donc leur âge maximal est infini, ou sinon ont met l'attribut age maximal que dans animal ?
        self.valeur_nutritive = 3
    
    def se_faire_manger(self) :
        self.vivant = False 
        return self.valeur_nutritive
        
   
class Animal(EtreVivant) :
    reproduction : Tuple[int,int]
    cout_reproduction : int
    
    def __init__(self,energie_initiale : int, energie_maximale : int, age_maximal : int, reproduction : Tuple[int, int], cout_reproduction : int) :
        super().__init__(energie_initiale, energie_maximale, age_maximal)
        self.reproduction = reproduction
        self.cout_reproduction = cout_reproduction
            
    def se_reproduire(self ) -> List["Animal"] : 
        if not self.vivant :
            return []       #Code peut être inutile car dans tous les cas pour rencontrer un animal, il doit être vivant
        if self.energie < self.cout_reproduction:
            return []                               #Doit avoir l'énergie necessaire pour se reporduire
        self.energie -= self.cout_reproduction      #Devra être ajuster pour être proportionnel au nombre d'enfants si demandé
        nombre_enfants = random.randint(self.reproduction[0], self.reproduction[1]) 
        
        enfants = []
        for _ in range(nombre_enfants) : #ChatGPT : underscore for _ ... convention lorsque la variable n'a pas besoin d'être utilisée dans la boucle
            enfant = type(self)( #chatGPT : type(self) nous renvoi la classe de l'objet self qui ici est la classe Lapin car on est dans sa définition
                energie_initiale=self.energie, 
                energie_maximale=self.energie_maximale,
                age_maximal=self.age_maximal,
                vivant = True,
                reproduction=self.reproduction,
                cout_reproduction=self.cout_reproduction
            )
            enfants.append(enfant) #On mettra plutôt environnement.append(enfant) quand l'environnement sera créer 
        return enfants


    #def se_deplacer(self, environnement):

class Lapin(Animal):
    valeur_nutritive : int
    def __init__(self):
        super().__init__(
            energie_initiale=10,
            energie_maximale=20,
            age_maximal=5,
            reproduction=(1, 3),
            cout_reproduction= 2)
        self.valeur_nutritive = 16
    
    def se_faire_manger(self) :
        self.vivant = False 
        return self.valeur_nutritive
            
        
class Renard(Animal) :
    def __init__(self):
        super().__init__(
            energie_initiale=25,
            energie_maximale= 50,
            age_maximal=3,
            reproduction = (1,5),
            cout_reproduction= 4)
        
#comment on fait pour optenir un diagramme déja ?


    
    








    


    