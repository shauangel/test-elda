import string

import nltk
from nltk.corpus import brown
from nltk import WordNetLemmatizer
from math import log
import itertools
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

if __name__ == "__main__":
    sents = ["Betsy and I live in New York.",
             "It pleased me doubly; to show off my fiancée and escape the rush of August in New York.",
             "Both of us were new to New York City, and had few or no friends.",
             "Betsy and I faced a six hour return trip to New York.",
             "All pertained to the earlier tests Howie and Quinn had undertaken together while Betsy and I were still in New York.",
             "She helped Carmen into the new dress.",
             "Is it something new for the trip?",
             "Emerging from the bathroom an hour later half asleep, she put the new nightgown on and climbed into bed.",
             "The Internet has allowed for the creation of thousands of new ways to give, both time and money.",
             "Do you think Jonathan might feel left out when the new baby comes?"]
    #print(len(_Sents))
    stopwords = nltk.corpus.stopwords.words('english')

    ##custom sentences
    #sentences = [nltk.word_tokenize(sen) for sen in sents]
    #words = [t.lower() for t in list(itertools.chain.from_iterable(sentences)) if t not in string.punctuation]

    ##brown
    words = [w for w in brown.words(categories='news') if w not in string.punctuation]
    sentences = brown.sents(categories='news')

    pmi = PMI(words, sentences)
    print(pmi.pmi("new", "york"))
    print("-"*20)
    print(pmi.pmi("new", "the"))
    print("-" * 20)
    print(pmi.pmi("york", "the"))

    ###test all pairwise
    #pairs = list(itertools.combinations(list(dict.fromkeys(words)), 2))
    #print(len(list(dict.fromkeys(words))))
    #print(len(pairs))

    title = ["x", "y", "p_x", "p_y", "p_xy", "pmi"]
