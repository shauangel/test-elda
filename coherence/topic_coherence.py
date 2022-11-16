from pmi import PMI
import itertools


class UCI:
    def __init__(self, tokens, sents, target_list):
        self._PMI = PMI(tokens, sents)
        self._Comb = list(itertools.combinations(target_list, 2))

    def coherence(self):
        pmi_sum = sum([self._PMI.pmi(p[0], p[1]) for p in self._Comb])
        print("pmi_sum: " + str(pmi_sum))
        return 2/(len(self._Comb)*(len(self._Comb)-1))*pmi_sum