import nltk
from nltk.corpus import brown
from TextAnalyze import TextAnalyze

from gensim.models import LdaModel
from gensim.corpora.dictionary import Dictionary
from gensim.models.coherencemodel import CoherenceModel

class LDA():
    def __init__(self, path):
        try:
            LdaModel.load(path)
        except:
            print("no such model...")

    def __init__(self, text, topic_num):
        self._RawText = text
        self._Dict = Dictionary(text)
        self._Corp = [self._Dict.doc2bow(t) for t in text]
        self.model = LdaModel(corpus=self._Corp, id2word=self._Dict, num_topics=topic_num)

    def getModel(self):
        return self.model

    def saveModel(self):
        self.model.save("/c_test/model")


if __name__ == "__main__":
    stopwords = nltk.corpus.stopwords.words('english')

    ##brown
    words = [w.lower() for w in brown.words(categories='news') if w not in string.punctuation]
    sentences = brown.sents(categories='news')

    pmi = PMI(words, sentences)
    #unique_w = list(dict.fromkeys(words))
    unique_w = ["game", "sport", "ball", "team"]

    ###test all pairwise
    pairs = list(itertools.combinations(unique_w[:], 2))
    for p in pairs:
        print("-" * 20)
        print(">>>>>PMI: " + str(pmi.pmi(p[0], p[1])))

    title = ["x", "y", "p_x", "p_y", "p_xy", "pmi"]

