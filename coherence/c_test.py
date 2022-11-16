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
    ## Step 1.
    print("step1,")
    news = [file for file in brown.fileids() if 'news' in brown.categories(file)]
    sents_list = [s for f in news[:5] for s in brown.sents(f)]
    print(len(sents_list))

    ## Step 2.
    print("step2,")
    analyzer = TextAnalyze()
    text = [analyzer.contentPreProcess(" ".join(s))[0] for s in sents_list]

    ## Step 3.
    print("step3,")
    lda = LDA(text, 5).getModel()
    for t in lda.print_topics():
        print(t)

