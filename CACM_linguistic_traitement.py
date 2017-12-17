import io
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle 

cacm = open("/home/lawliet/Downloads/FRI-W/Les cours.IS3013AA.Data/CACM/cacm.all",'r')
file = open("/home/lawliet/Downloads/FRI-W/Les cours.IS3013AA.Data/CACM/common_words",'r')
stopWords = file.read().lower().splitlines() + ['.',',',':',' ','  ','   ',';', '    ', ')', '(', '[', ']', '{', '}']


corpus_v1 = cacm.read()
corpus_v1 = corpus_v1.split('\n')
corpus = []
l = []
for i in range(len(corpus_v1)):
	if (corpus_v1[i][:2] == '.I'):
		corpus.append(l)
		l = []
	elif (corpus_v1[i][:2] == '.T' or corpus_v1[i][:2] == '.W' or corpus_v1[i][:2] == '.K'):
		j = i+1
		while (corpus_v1[j][0] != '.'):
			word_tokens = word_tokenize(corpus_v1[j].lower())
			filtered_sentence = [w for w in word_tokens if not w in stopWords]
			l.extend(filtered_sentence)
			j += 1


corpus.append(l)
corpus.pop(0)
print corpus, len(corpus)


collections = open("CACM_treated.txt",'w')
pickle.dump(corpus, collections)
collections.close()

cacm.close()
file.close()