import numpy as np
from heapq import heappush, heappop

def calculer_h(noeud, couts):
    if noeud.estBut():
        return 0
    temp = np.delete(couts[noeud.p:], noeud.affectations, 1)
    return max(np.amin(temp, 1).sum(), np.amin(temp, 0).sum())

class Noeud:
    def __init__(self, n, couts, g=0, p=0, affectations=list()):
        self.n = n
        self.g = g
        self.p = p
        self.affectations = affectations
        self.h = calculer_h(self, couts)
        self.f = self.g + self.h
    
    def estBut(self):
        return self.p == self.n
    
    def developpe(self, couts):
        heritiers = list()
        
        for i, cout in enumerate(couts[self.p]):
            if i not in self.affectations:
                heritiers.append(Noeud(self.n, couts, g=self.g+cout, p=self.p+1, affectations=self.affectations+[i]))
        
        return heritiers
    
    def __lt__(self, other):
        return self.f < other.f

def affectations(couts):
    n = len(couts)
    OUVERT = [Noeud(n, couts)]
    nb_noeuds_ouverts = 1

    while len(OUVERT) > 0:
        
        noeud = heappop(OUVERT)
        
        if noeud.estBut():
            break
        
        for heritier in noeud.developpe(couts):
            heappush(OUVERT, heritier)
            nb_noeuds_ouverts += 1
    
    return noeud.affectations, nb_noeuds_ouverts


if __name__ == '__main__':
    
    couts = np.random.randint(1000, size=(10, 10))
    print(affectations(couts))