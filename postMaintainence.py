import _db
from StackData import StackData
from TextAnalyze import TextAnalyze
import csv
import re


def save_models(data):
    _db.TOPIC_DATA_COLLECTION.insert_one(data)


# --> load data from db <--
def load_data():
    print("Linking database...")
    parsed = _db.OUTER_DATA_COLLECTION.find()
    articles = []
    for post in parsed:
        try:
            text = [post['question']['abstract']]
            text += [i['abstract'] for i in post['answers']]
            articles.append(text)
        except:
            print(post['link'])

    return articles


def generate_tags(text, topic_num, model_num):
    print("Train model...")
    model, c_s = t_a.eLDATopicModeling(text, topic_num, model_num)
    topics = []
    print("Display topics...")
    for t in model.print_topics(-1):
        words = re.findall(r'\*"(.*?)"', t[1])
        p = re.findall(r'(\d*.\d*?)\*', t[1])
        topics.append({"tokens":words, "prob":p})
        print(words)
    info = {"num_t":topic_num, "num_m":model_num, "topics":topics}
    save_models({**info, **c_s})
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
    print(len(data))
    t_a = TextAnalyze()
    raw_text = [" ".join(t) for t in data]

    # 500post 250t 5m 5iterations
    print("500post 250t 5m 5iterations...")
    text = [t_a.contentPreProcess(i)[0] for i in raw_text[:500]]
    for i in range(5):
        print("Starts iteration " + str(i))
        generate_tags(text, 250, 5)
        print("Finished")

    # 100post 50t 5m 5slots
    print("100post 50t 5m 5slots...")
    for i in range(5):
        print("Start slot " + str(i))
        text = [t_a.contentPreProcess()[0] for w in raw_text[i*100:(i+1)*100]]
        model = generate_tags(text, 50, 5)
        print("Finished")