import _db
from StackData import StackData
from TextAnalyze import TextAnalyze
import csv


# --> load data from db <--
def load_data():
    print("Linking database...")
    parsed = _db.OUTER_DATA_COLLECTION.find()
    return [i for i in parsed]


def generate_tags(text_list):
    t_a = TextAnalyze()
    corpus = [t_a.contentPreProcess(i)[0] for i in text_list]
    with open('corpus.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for article in corpus:
            writer.writerow(article)
    t_a.eLDATopicModeling(corpus, 50, 5)


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
