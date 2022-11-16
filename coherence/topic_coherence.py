from pmi import PMI
import itertools
from math import log
from scipy import spatial



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
        self._Targ = self.sortByProb(target_list)
        self._Comb = list(itertools.combinations(self._Targ, 2))

    def sortByProb(self, target_list):
        prob_list = {k:self._PMI.p(k) for k in target_list}
        prob_list = dict(sorted(prob_list.items(), key=lambda item: item[1], reverse=True))
        return list(prob_list.keys())


    def conditionalProb(self, x, y):
        pxy = self._PMI.pxy(x, y)
        py = self._PMI.p(y)
        print("P(" + x + ", " + y + "): " + str(pxy/py))
        return pxy/py
    def coherence(self):
        condP_sum = sum([log(self.conditionalProb(p[1], p[0]), 2) for p in self._Comb])
        print("condP_sum: " + str(condP_sum))
        print(self._Comb)
        return (2/(len(self._Comb)*(len(self._Comb)-1)))*condP_sum

class NPMI:
    def __init__(self, tokens, sents, target_list):
        self._PMI = PMI(tokens, sents)
        self._Comb = list(itertools.combinations(target_list, 2))

    def coherence(self):
        npmi_sum = sum([self._PMI.npmi(p[0], p[1]) for p in self._Comb])
        print("npmi_sum: " + str(npmi_sum))
        print(self._Comb)
        return (2/(len(self._Comb)*(len(self._Comb)-1)))*npmi_sum

class Vector:
    def __init__(self, tokens, sents, target_list):
        self._PMI = PMI(tokens, sents)
        self._Targ = target_list
        self._Comb = list(itertools.combinations(target_list, 2))

    #generate context vector
    def v(self, x):
        contextV = [self._PMI.npmi(x, i) for i in self._Targ]
        print("v_" + x + ": ")
        print(contextV)
        return contextV

    #cosine similarity
    def cos_sim(self, x, y):
        cosine_similarity = 1 - float(spatial.distance.cosine(x, y))
        print("cos: " + str(cosine_similarity))
        return cosine_similarity

    ##coherence score
    def coherence(self):
        v_list = [self.v(x) for x in self._Targ]
        vec_comb = list(itertools.combinations(v_list, 2))
        print("--"*10)
        print(vec_comb)
        print("--" * 10)
        word_co = (2/(len(vec_comb)*(len(vec_comb)-1)))
        cos = sum([self.cos_sim(v[0], v[1]) for v in vec_comb])
        return word_co*cos