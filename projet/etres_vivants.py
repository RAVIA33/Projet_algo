from typing import Tuple
from typing import List
import random
from parametres import *



class EtreVivant  : 
    #attributs communs à tous les êtres vivants
    energie: int                  
    energie_maximale : int          
    age_maximal : int               
    age : int                       
    vivant : bool  
    valeur_nutritive : int                 
    
    def __init__(self,  energie_initiale : int, energie_maximale : int, age_maximal:float, valeur_nutritive: int) :
        self.energie = energie_initiale
        self.energie_maximale = energie_maximale
        self.age = 0
        self.age_maximal = age_maximal
        self.vivant = True
        self.valeur_nutritive = valeur_nutritive 

    def est_vivant(self) -> bool:
        return self.energie
    
    def perdre_energie(self, montant: int) -> None:
        self.energie -= montant
        if self.energie <= 0:
            self.energie = 0
            self.vivant = False

    def mettre_a_jour(self) -> None:
        #fonction de vieillissemnet
        self.age += 1
        if self.age > self.age_maximal:
            self.vivant = False
    
class Plante(EtreVivant) : 
    def __init__(self):
        super().__init__(
            energie_initiale=plante_valeur_nutritive,
            energie_maximale=plante_valeur_nutritive,
            age_maximal=float("inf"),
            valeur_nutritive=plante_valeur_nutritive)
    
    
    def se_faire_manger(self) :
        self.vivant = False 
        return self.valeur_nutritive
    
    def vieillir(self):
        pass #les plantes de "vieillisent pas"
        
   
class Animal(EtreVivant) :
    # reproduction : Tuple[int,int]
    # cout_reproduction : int
    
    def __init__(self, energie_initiale: int, energie_maximale: int, age_maximal: int,
                 reproduction: Tuple[int, int], cout_reproduction: int, cout_deplacement: int,
                 valeur_nutritive: int):
        super().__init__(energie_initiale, energie_maximale, age_maximal, valeur_nutritive)
        self.reproduction = reproduction
        self.cout_reproduction = cout_reproduction
        self.cout_deplacement = cout_deplacement
            
    def se_reproduire(self ) -> List["Animal"] : 
        if self.energie < self.cout_reproduction : #ne peut pas se reproduire si sont énergie est insuffisante
            return []       
        
        #réduction de l'énergie lors de la reproduction 
        self.perdre_energie(self.cout_reproduction)

        #génère des enfants lors de la collision, entre 0 et 3 aléatoirement
        nombre_enfants = random.randint(*self.reproduction)#* "décompacte" ces deux valeurs pour les passer comme arguments séparés à random.randint 
        enfants = []
        for _ in range(nombre_enfants) : #ChatGPT : underscore for _ ... convention lorsque la variable n'a pas besoin d'être utilisée dans la boucle
            enfant = type(self)( #chatGPT : type(self) nous renvoi la classe de l'objet self qui ici est la classe Lapin car on est dans sa définition
                energie_initiale=self.energie_maximale,  #energie initiale définit pour chaque entité comme l'énergie max
                energie_maximale=self.energie_maximale,
                age_maximal=self.age_maximal,
                reproduction=self.reproduction,
                cout_reproduction=self.cout_reproduction,
                cout_deplacement=self.cout_deplacement,
                valeur_nutritive=self.valeur_nutritive)
            
            enfants.append(enfant) #on mettra plutôt environnement.append(enfant) quand l'environnement sera créer 
        return enfants


class Lapin(Animal):
    # valeur_nutritive : int
    # energie_initiale= 10
    def __init__(self, 
                energie_initiale=lapin_energie_initiale, 
                energie_maximale=lapin_energie_maximale, 
                age_maximal=lapin_age_maximal, 
                reproduction=(lapin_reproduction_min,lapin_reproduction_max),
                cout_reproduction=lapin_couts_reproduction, 
                cout_deplacement=lapin_cout_deplacement,
                valeur_nutritive=lapin_valeur_nutritive):
        super().__init__(
            energie_initiale=energie_initiale,
            energie_maximale=energie_maximale,
            age_maximal=age_maximal,
            reproduction=reproduction,
            cout_reproduction=cout_reproduction,
            cout_deplacement=cout_deplacement,
            valeur_nutritive=valeur_nutritive)
    
    def mettre_a_jour(self):
        super().mettre_a_jour()  #vieillissement
        if self.vivant:
            self.perdre_energie(self.cout_deplacement)

    def se_faire_manger(self) :
        self.vivant = False 
        return self.valeur_nutritive
    
    def vieillir(self):
        self.age += 1
        if self.age > self.age_maximal:
            self.vivant = False
        
        
class Renard(Animal) :
    def __init__(self, 
                energie_initiale=renard_energie_initiale, 
                energie_maximale=renard_energie_maximale, 
                age_maximal=renard_age_maximal, 
                reproduction=(renard_reproduction_min, renard_reproduction_max), 
                cout_reproduction=renard_couts_reproduction, 
                cout_deplacement=renard_couts_deplacement, 
                valeur_nutritive=0):
        super().__init__(
            energie_initiale=energie_initiale,
            energie_maximale=energie_maximale,
            age_maximal=age_maximal,
            reproduction=reproduction,
            cout_reproduction=cout_reproduction,
            cout_deplacement=cout_deplacement,
            valeur_nutritive=valeur_nutritive) #nulle car les renards ne peuvent pas être mangé
        
    def vieillir(self):
        self.age += 1
        if self.age > self.age_maximal:
            self.vivant = False
#comment on fait pour optenir un diagramme déja ?


    
    








    


    