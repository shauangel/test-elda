import json
import re
from gensim.models import EnsembleLda

path = "data/exp2/draw/t_5/"
file = "test_result_draw.json"

if __name__ == "__main__":
    with open(path+file, "r", encoding='utf-8')as f:
        result = json.load(f)
        f.close()

    for t in result[4]['050']:
        #print(t[1])
        words = re.findall(r'\*"(.*?)"', t[1])
        print(words)
    #