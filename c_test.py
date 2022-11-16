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


if __name__ == "__main__":
    ## Step 1.
    print("step1,")
    news = [file for file in brown.fileids() if 'news' in brown.categories(file)]
    word_list = [brown.words(file) for file in news]


    ## Step 2.
    print("step2,")
    analyzer = TextAnalyze()
    text = [analyzer.contentPreProcess(" ".join(l))[0] for l in word_list]

    print(len(text))



