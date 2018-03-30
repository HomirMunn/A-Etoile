"""\package affectations
Un super package qui utilise l'algorithme A-Etoile pour parcourir un
graphe qui va chercher le meilleur ensemble d'affectations pour un tableau de couts.
"""

import numpy as np
from heapq import heappush, heappop

class Noeud:
	"""Classe décrivant un noeud du graphe."""
	
    def __init__(self, n, couts, g=0, p=0, affectations=list()):
		"""Constructeur de noeud.
		
		\param n: Entier qui correspond à la profondeur maximale du graphe.
		\param couts : Table des couts.
		\param g: Cout d'un chemin optimal du premier noeud à celui-ci.
		\param p: Profondeur du noeud.
		\param affectations: Liste contenant toutes les affectations de ce noeud.
		"""
		
        self.n = n
        self.g = g
        self.p = p
        self.affectations = affectations
        self.h = calculer_h(self, couts)
        self.f = self.g + self.h
    
    def estBut(self):
		"""Renvoie True si le noeud est un but et False sinon.
		
		\return: True si le noeud est un but et False sinon.
		"""
		
        return self.p == self.n
    
    def developpe(self, couts):
		"""Developpe le noeud.
		
		\param couts: La table des couts.
		\return: La liste des noeuds developpes à partir de celui-ci.
		"""
		
        heritiers = list()
        
        for i, cout in enumerate(couts[self.p]):
            if i not in self.affectations:
                heritiers.append(Noeud(self.n, couts, g=self.g+cout, p=self.p+1, affectations=self.affectations+[i]))
        
        return heritiers
    
    def __lt__(self, other):
		"""Redéfini l'opérateur lesser than (<) pour les noeuds.
		
		\param other: un autre noeud
		\return: True si le f du noeud est plus petit que celui d'un autre et False sinon.
		"""
		
        return self.f < other.f


def calculer_h(noeud, couts):
	"""Calcul l'heuristique pour un noeud.
	
	\param noeud: Le noeud dont on veut calculer l'heuristique.
	\param couts: La table des couts.
	\return: L'heuristique du noeud.
	"""
	
    if noeud.estBut():
        return 0
    temp = np.delete(couts[noeud.p:], noeud.affectations, 1)
    return max(np.amin(temp, 1).sum(), np.amin(temp, 0).sum())


def affectations_optimales(couts):
	"""Retourne les affectations optimales pour une table de couts donnée.
	
	\param couts: La table de couts dont on veut trouver les affectations optimales.
	\return: Un tuple contenant la liste des affectations optimales et le nombre de noeuds développés.
	"""
	
    n = len(couts)
    OUVERT = [Noeud(n, couts)]
    nb_noeuds_developpes = 1

    while len(OUVERT) > 0:
        
        noeud = heappop(OUVERT)
        
        if noeud.estBut():
            break
        
        for heritier in noeud.developpe(couts):
            heappush(OUVERT, heritier)
            nb_noeuds_developpes += 1
    
    return noeud.affectations, nb_noeuds_developpes


if __name__ == '__main__':
    
    couts = np.random.randint(1000, size=(10, 10))
    print(affectations_optimales(couts))
