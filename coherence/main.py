##dependecies
import string
import itertools
import nltk
from nltk.corpus import brown
##custom
from pmi import PMI
from topic_coherence import UCI


if __name__ == "__main__":
    stopwords = nltk.corpus.stopwords.words('english')

    ##brown
    words = [w.lower() for w in brown.words(categories='news') if w not in string.punctuation]
    sentences = brown.sents(categories='news')

###pmi

    pmi = PMI(words, sentences)
    print(">>>>>PMI: " + str(pmi.pmi("york", "city")))
    #unique_w = list(dict.fromkeys(words))
    #["weather", "york", "the", "team"]
    unique_w = ["game", "sport", "ball", "team"]

    """
    ###test all pairwise
    pairs = list(itertools.combinations(unique_w[:], 2))
    for p in pairs:
        print("-" * 20)
        print(">>>>>PMI: " + str(pmi.pmi(p[0], p[1])))

    #title = ["x", "y", "p_x", "p_y", "p_xy", "pmi"]
    """
    ###uci
    #c_model = UCI(words, sentences, unique_w)
    #print(c_model.coherence())