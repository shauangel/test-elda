import _db
from StackData import StackData
from TextAnalyze import TextAnalyze
import csv
import re
import math
from collections import Counter


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
    t_a = TextAnalyze()
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


def counter_cosine_similarity(listA, listB):
    c1 = Counter(listA)
    c2 = Counter(listB)
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return round(dotprod / (magA * magB))


if __name__ == "__main__":
    """
    data = load_data()
    print(len(data))
    t_a = TextAnalyze()
    raw_text = [" ".join(t) for t in data]

    # 500post 250t 5m 5iterations
    #print("500post 250t 5m 5iterations...")
    #text = [t_a.contentPreProcess(i)[0] for i in raw_text[:500]]
    #for i in range(5):
    #    print("Starts iteration " + str(i))
    #    generate_tags(text, 250, 5)
    #    print("Finished")

    # 100post 50t 5m 5slots
    print("100post 50t 5m 5slots...")
    for i in range(5):
        print("Start slot " + str(i))
        text = [t_a.contentPreProcess(w)[0] for w in raw_text[i*100:(i+1)*100]]
        model = generate_tags(text, 50, 5)
        print("Finished")
    """
    # finding threshold
    data = _db.TOPIC_DATA_COLLECTION.find({"num_t" : 50})
    title = ["c_v", "u_mass", "c_uci", "c_npmi", "token", "prob"]
    per_topic = []
    per_topic.append(title)
    for m in data:
        for idx in range(len(m['topics'])):
            tokens = ", ".join(m['topics'][idx]['tokens'])
            probs = ", ".join(m['topics'][idx]['prob'])
            t = [m['c_v_per_topic'][idx],
                 m['u_mass_per_topic'][idx],
                 m['c_uci_per_topic'][idx],
                 m['c_npmi_per_topic'][idx],
                 tokens, probs]
            print(t)
            per_topic.append(t)
    
    with open("result.csv", 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(per_topic)
    """
    t_list = []
    with open("result.csv", 'r', encoding='utf-8') as f:
        topics = csv.reader(f)
        t_list = [i[4].split(", ") for i in topics]

    # n^2 calculate similarity of list
    for i in range(len(t_list)):
        print(t_list[i])
        print([counter_cosine_similarity(t_list[i], t_list[j]) for j in range(len(t_list))])

    """
