import _db
from StackData import StackData
from TextAnalyze import TextAnalyze
import csv
import re


# --> load data from db <--
def load_data():
    print("Linking database...")
    parsed = _db.OUTER_DATA_COLLECTION.find()
    return [i for i in parsed]


def generate_tags(text_list, corpus_file, result_file):
    t_a = TextAnalyze()
    corpus = [t_a.contentPreProcess(i)[0] for i in text_list]
    with open( corpus_file+'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for article in corpus:
            writer.writerow(article)
        csvfile.close()
    model = t_a.eLDATopicModeling(corpus, 100, 5)
    tokens = []
    topics = []
    for t in model.print_topics(-1):
        words = re.findall(r'\*"(.*?)"', t[1])
        p = re.findall(r'(\d*.\d*?)\*', t[1])
        tokens += words
        distribution_dict = {words[i]:p[i] for i in range(len(words))}
        topics.append(distribution_dict)
        print(distribution_dict)
    tokens = list(dict.fromkeys(tokens))
    with open( result_file+'.csv', 'w', newline='') as csvfile:
        dict_writer = csv.DictWriter(csvfile, fieldnames=tokens)
        for t in topics:
            writer.writerow(t)
    return model


# --> parse more posts <--
def parse_full_post():
    # step 1. get post_id list
    print("Linking db...")
    all_data = _db.OUTER_DATA_CACHE_COLLECTION.find()
    print("Get post list...")

    # step 2. check current parsing progress
    parsed = _db.OUTER_DATA_COLLECTION.find()
    print("Check current progress...")
    curr = len([i for i in parsed])

    # step 3. continue progress
    print("Start parsing...")
    i = 1
    for p in all_data:
        # iterate to the latest progress
        if i <= curr:
            print(i)
            i += 1
            continue
        else:
            # request for post information until it hits the limit
            try:
                print(p['title'])
                parser = StackData(p['link'])
                _db.OUTER_DATA_COLLECTION.insert_one(parser.showData())
                i += 1
            except Exception:
                print(i)
                break


if __name__ == "__main__":
    data = load_data()
