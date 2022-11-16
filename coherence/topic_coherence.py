from pmi import PMI
import itertools
from math import log


class UCI:
    def __init__(self, tokens, sents, target_list):
        self._PMI = PMI(tokens, sents)
        self._Comb = list(itertools.combinations(target_list, 2))

    def coherence(self):
        pmi_sum = sum([self._PMI.pmi(p[0], p[1]) for p in self._Comb])
        print("pmi_sum: " + str(pmi_sum))
        print(self._Comb)
        return (2/(len(self._Comb)*(len(self._Comb)-1)))*pmi_sum

class UMass:
    def __init__(self, tokens, sents, target_list):
        self._PMI = PMI(tokens, sents)
        self._Comb = list(itertools.combinations(target_list, 2))

    def conditionalProb(self, x, y):
        pxy = self._PMI.pxy(x, y)
        py = self._PMI.px(y)
        print("P(" + x + ", " + y + "): " + str(pxy/py))
        return pxy/py
    def coherence(self):
        condP_sum = sum([log(self.conditionalProb(p[1], p[0]), 2) for p in self._Comb])
        print("condP_sum: " + str(condP_sum))
        print(self._Comb)
        return (2/(len(self._Comb)*(len(self._Comb)-1)))*condP_sum