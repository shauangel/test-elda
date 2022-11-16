import string

import nltk
from nltk.corpus import brown
from nltk import WordNetLemmatizer
from math import log
import itertools

from gensim.models import Lda
from gensim.corpora.dictionary import Dictionary
from gensim.models.coherencemodel import CoherenceModel

wnl=WordNetLemmatizer()


#_Fdist = nltk.FreqDist([wnl.lemmatize(w.lower()) for w in brown.words(categories='news')])

#_Sents = [[wnl.lemmatize(j.lower()) for j in i] for i in brown.sents(categories='news')]
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
        return log(self.pxy(x, y)/(self.p(x) * self.p(y)),2)

class LDA():
    def __init__(self, path):
        try:
            Lda.load(path)
        except:
            print("no such model...")
    def __init__(self, corpus, dictionary, topic_num):
        self.model = Lda(corpus=corpus, id2word=dictionary, num_topics=topic_num)
        self._Dict = dictionary
        self._Corp = corpus



if __name__ == "__main__":
    #print(len(_Sents))
    stopwords = nltk.corpus.stopwords.words('english')

    ##brown
    words = [w.lower() for w in brown.words(categories='news') if w not in string.punctuation]
    sentences = brown.sents(categories='news')

    pmi = PMI(words, sentences)
    #print(pmi.pmi("new", "york"))
    #print("-"*20)
    #print(pmi.pmi("new", "the"))
    #print("-" * 20)
    #print(pmi.pmi("york", "the"))
    #print("-" * 20)
    #print(pmi.pmi("new", "sport"))
    #unique_w = list(dict.fromkeys(words))
    unique_w = ["game", "sport", "ball", "team"]
    #print(unique_w[:10])

    ###test all pairwise
    pairs = list(itertools.combinations(unique_w[:], 2))
    for p in pairs:
        print("-" * 20)
        print(">>>>>PMI: " + str(pmi.pmi(p[0], p[1])))

    title = ["x", "y", "p_x", "p_y", "p_xy", "pmi"]
