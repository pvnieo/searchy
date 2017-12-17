import pickle


f = open("CACM_treated.txt",'r')
collections = pickle.load(f)


dictionnaire = {}
dic_terms = {}
i = 1
for L in collections :
	k = collections.index(L)+1
	for mot in L :
		if mot not in dic_terms.keys():
			dic_terms[mot] = i
			i+= 1
		if dic_terms[mot] in dictionnaire.keys() :
			if k not in dictionnaire[dic_terms[mot]]:
				dictionnaire[dic_terms[mot]].append(k)
		else : 
			dictionnaire[dic_terms[mot]] = [k]


for mot in dictionnaire.keys():
	l = dictionnaire[mot]
	l.sort()
	dictionnaire[mot] = l


file = open("indexInverse.txt","w")
pickle.dump(dictionnaire,file)
file.close()

file = open("dic_terms.txt","w")
pickle.dump(dic_terms,file)
file.close()

f.close()

