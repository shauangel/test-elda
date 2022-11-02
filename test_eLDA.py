from gensim.models import EnsembleLda
from gensim.corpora.dictionary import Dictionary
from gensim.models.coherencemodel import CoherenceModel
#from gensim.models import LdaModel

from TextAnalyze import TextAnalyze
import json
from pathlib import Path
#from gensim.parsing.preprocessing import preprocess_string, strip_punctuation, strip_numeric

data_path = "data/"
resource_file = "vote100_web-crawler_full_post.json"
result_dir = data_path + "models/" + resource_file.split("_")[1]

def trainEnsembleLDA(num_topic, num_model):
    ##train elda
    elda = EnsembleLda(corpus=voteQ_corpus, id2word=voteQ_dictionary, num_topics=num_topic, num_models=num_model)
    try:
        elda.save(result_dir+ "/elda_model_"+str(num_topic))
    except:
        Path(result_dir).mkdir(parents=True, exist_ok=True)
        elda.save(result_dir + "/elda_model_" + str(num_topic))
    return elda

if __name__ == "__main__":

    ##loading resources
    with open(data_path+resource_file, "r", encoding='utf-8') as f:
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

    print("-" * 10 + "Creating Corpus" + "-" * 10)
    ##transfer to bag-of-words
    voteQ_dictionary = Dictionary(raw_texts)
    print("Total tokens in corpus: " + str(len(voteQ_dictionary)))
    voteQ_corpus = [voteQ_dictionary.doc2bow(text) for text in raw_texts]

    #num_topic = 30
    num_model = 5
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

    ##Visulize train result
        print("-" * 10 + "Test Result" + "-" * 10)
        #Statistical Measure
        print("AvgTopic: " + str(averageTopic/totalTest).zfill(3))
        print("Success: " + str(totalTest - failed).zfill(3))
        print("Failed: " + str(failed).zfill(3))

        #Coherence Measure
        texts = [[voteQ_dictionary[word_id] for word_id, freq in doc] for doc in voteQ_corpus]
        c_v = ""
        c_v_per_t = []
        u_mass = ""
        u_mass_per_t = []
        ##c_v measure
        cm_c_v_model = CoherenceModel(model=elda, texts=texts, corpus=voteQ_corpus, dictionary=voteQ_dictionary, coherence="c_v")
        try:
            c_v = "{:5.4f}".format(cm_c_v_model.get_coherence())
            c_v_per_t = cm_c_v_model.get_coherence_per_topic()
            ##aggregate value
            print("C_v Measure: " + c_v)
            ##each topic's value
            print(c_v_per_t)
        except:
            print("no stable topic found...")

        ##u_mass measure
        cm_u_mass_model = CoherenceModel(model=elda, corpus=voteQ_corpus, dictionary=voteQ_dictionary, coherence="u_mass")
        try:
            u_mass = "{:5.4f}".format(cm_u_mass_model.get_coherence())
            u_mass_per_t = cm_u_mass_model.get_coherence_per_topic()
            print("U_mass Measure: " + u_mass)
            print(u_mass_per_t)
        except:
            print("no stable topic found...")

        #Display result
        test_result.append({
            str(num_topic).zfill(3):topics,
            "success":totalTest - failed,
            "failed":failed,
            "avg_topic":averageTopic/totalTest,
            "c_v":c_v,
            "c_v_per_topic":c_v_per_t,
            "u_mass":u_mass,
            "u_mass_per_topic":u_mass_per_t
        })
        print("-" * 10 + "Finished" + "-" * 10)


    with open(result_dir + "/test_result_" + resource_file.split("_")[1] + ".json", "w", encoding="utf-8") as f:
        json.dump(test_result, f)
        f.close()





