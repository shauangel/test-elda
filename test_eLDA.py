import gensim
from gensim.test.utils import common_texts
from gensim.corpora.dictionary import Dictionary
from gensim.models import EnsembleLda

from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel

from TextAnalyze import TextAnalyze
import json

if __name__ == "__main__":

    ##loading resources
    with open("voteQ_full_post.json", "r", encoding='utf-8') as f:
        data = json.load(f)
        f.close()

    ##initialize text analyzer
    analyzer = TextAnalyze()

    ##collect raw text (test 10 post)
    raw_texts = []
    for q in data[:50]:
        print(q['question']['title'])
        #curr_text = []
        tokens, doc = analyzer.contentPreProcess(q['question']['abstract'])
        #curr_text += tokens
        """
        for ans in q['answers']:
            print(ans['id'])
            tokens, doc = analyzer.contentPreProcess(ans['abstract'])
            curr_text += tokens
        """
        raw_texts.append(tokens)
        print("--"*10)


    ##transfer to bag-of-words
    voteQ_dictionary = Dictionary(raw_texts)
    print(len(voteQ_dictionary))
    voteQ_corpus = [voteQ_dictionary.doc2bow(text) for text in raw_texts]

    ##train elda
    lda = EnsembleLda(corpus=voteQ_corpus, id2word=voteQ_dictionary, num_topics=20, num_models=10)
    lda.save("test_elda")


    lda = EnsembleLda.load("test_elda")
    for t in lda.print_topics():
        print(t)


