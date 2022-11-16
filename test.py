from nltk.corpus import brown

news = [file for file in brown.fileids() if 'news' in brown.categories(file)]
word_list = [brown.sents(file) for file in news]

#for words in word_list:
print(word_list[0])