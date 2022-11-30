import csv
import math
from collections import Counter

def counter_cosine_similarity(listA, listB):
    c1 = Counter(listA)
    c2 = Counter(listB)
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return round(dotprod / (magA * magB), 3)

if __name__ == "__main__":
    t_list = []
    with open("result.csv", 'r', encoding='utf-8') as f:
        topics = csv.reader(f)
        t_list = [i[4].split(", ") for i in topics]

    # n^2 calculate similarity of list
    score_list = []
    for i in range(len(t_list)):
        score_list.append([counter_cosine_similarity(t_list[i], t_list[j]) for j in range(len(t_list))])

    with open("sim.csv", "w", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(score_list)

