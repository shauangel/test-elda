import gensim
from TextAnalyze import TextAnalyze
import json

##loading resources
with open("voteQ_full_post.json", "r", encoding='utf-8') as f:
    data = json.load(f)
    f.close()

##initialize text analyzer
analyzer = TextAnalyze()


