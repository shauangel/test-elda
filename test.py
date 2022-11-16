import string
import nltk
from nltk.corpus import brown
from
stopwords = nltk.corpus.stopwords.words('english')

news = [file for file in brown.fileids() if 'news' in brown.categories(file)]
word_list = [brown.words(file) for file in news]
corpus = [[w.lower() for w in l if w not in string.punctuation and w not in stopwords] for l in word_list]

print(corpus[0])