import gensim
from gensim.test.utils import common_texts
from gensim.corpora.dictionary import Dictionary
from gensim.models import EnsembleLda

from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel

from TextAnalyze import TextAnalyze
import json
#from gensim.parsing.preprocessing import preprocess_string, strip_punctuation, strip_numeric


def trainEnsembleLDA(num_topic, num_model):
    ##train elda
    elda = EnsembleLda(corpus=voteQ_corpus, id2word=voteQ_dictionary, num_topics=num_topic, num_models=num_model)
    elda.save("test_elda")
    return elda

if __name__ == "__main__":

    ##loading resources
    with open("voteQ_full_post.json", "r", encoding='utf-8') as f:
        data = json.load(f)
        f.close()

    ##initialize text analyzer
    analyzer = TextAnalyze()

    ##collect raw text (test 10 post)
    raw_texts = []
    print("-"*10 + "Start Pre-Process" + "-"*10)
    for q in data:
        print(q['question']['title'])

        #collect tokens from post
        tokens, doc = analyzer.contentPreProcess(q['question']['abstract'])
        raw_texts.append(tokens)

        print("--" * 10)

    print("-" * 10 + "Creating Corpus" + "-" * 10)
    ##transfer to bag-of-words
    voteQ_dictionary = Dictionary(raw_texts)
    print("Total tokens in corpus: " + str(len(voteQ_dictionary)))
    voteQ_corpus = [voteQ_dictionary.doc2bow(text) for text in raw_texts]

    #num_topic = 30
    num_model = 15
    totalTest = 1
    print("-" * 10 + "Start Training Models" + "-" * 10)

    test_result = []
    #test for num_topic = 10 ~ = 100
    for num_topic in range(10, 100, 10):
        failed = 0
        averageTopic = 0
        print("num_topic: " + str(num_topic).zfill(3))
        print("num_model: " + str(num_model).zfill(3))
        for i in range(totalTest):
            print("Test " + str(i).zfill(2) + ": ")
            elda = trainEnsembleLDA(num_topic, num_model)
            topics = []
            try:#test if stable topics exist
                for t in elda.print_topics(-1):
                    topics.append(t)
                    averageTopic += 1
                    print(t)
            except:
                failed+=1
                topics = "err"
                print("no stable topic detected~~~")
        print("-" * 10 + "Test Result" + "-" * 10)

        print("AvgTopic: " + str(averageTopic/totalTest).zfill(3))
        print("Sucess: " + str(totalTest - failed).zfill(3))
        print("Failed: " + str(failed).zfill(3))
        test_result.append({
            str(num_topic).zfill(3):topics,
            "success":totalTest - failed,
            "failed":failed,
            "avg_topic":averageTopic/totalTest
        })

    with open("test_result_" + str(num_model) + "_models.json", "w", encoding="utf-8") as f:
        json.dump(test_result, f)
        f.close()
    #lda = EnsembleLda.load("test_elda")



