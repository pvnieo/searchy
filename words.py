import nltk
import string
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

STOP_WORDS = set(nltk.corpus.stopwords.words('english'))
PONCTUATION = string.punctuation
with open("data/CACM/common_words", 'r') as common_words:
    STOP_WORDS.update(set(common_words.read().lower().splitlines()))

wordnet_lemmatizer = WordNetLemmatizer()
porter_stemmer = PorterStemmer()

def tokenize(text):
    tokens = []
    for char in PONCTUATION:
        text = text.replace(char, ' ')
    for token in [t.lower() for t in nltk.word_tokenize(text)]:
        if token in STOP_WORDS:
            continue
        tokens.append(token)
    return tokens

def lemmatize(tokens):
    lemmatized_tokens = {}
    for token in tokens:
        term = porter_stemmer.stem(wordnet_lemmatizer.lemmatize(token))
        if term not in lemmatized_tokens:
            lemmatized_tokens[term] = 1
        else:
            lemmatized_tokens[term] += 1
    return list(lemmatized_tokens.items())

def process(text):
    return lemmatize(tokenize(text))