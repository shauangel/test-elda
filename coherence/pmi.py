import nltk
from nltk import WordNetLemmatizer
from math import log
wnl=WordNetLemmatizer()


class PMI:
    def __init__(self, tokens, sents):
        self._Fdist = nltk.FreqDist([wnl.lemmatize(w.lower()) for w in tokens])
        self._Sents = [[wnl.lemmatize(j.lower()) for j in i] for i in sents]

    #計算word x出現的機率
    def p(self, x):
        p_x = self._Fdist[x]/float(len(self._Fdist))
        print("Calculate p(" + x + ")...")
        print(str(self._Fdist[x])+ "/" + str(len(self._Fdist)) + "= " + str(p_x))
        return p_x

    #計算word x, word y出現在同一個sentence的機率
    def pxy(self, x, y):
        p_xy = (len(list(filter(lambda s : x in s and y in s ,self._Sents)))+1) / float(len(self._Sents))
        print("Calculate p(" + x + ", " + y + ")...")
        print(str(len(list(filter(lambda s : x in s and y in s ,self._Sents)))) + "/" + str(len(self._Sents)) + "=" + str(p_xy))
        return p_xy

    #計算pmi
    def pmi(self, x, y):
        pmi_score = log(self.pxy(x, y)/(self.p(x) * self.p(y)),2)
        print("pmi: " + str(pmi_score))
        return pmi_score

