# stdlib
import string
# 3p
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

STOP_WORDS = set(nltk.corpus.stopwords.words('english'))
PONCTUATION = string.punctuation
with open("data/CACM/common_words", 'r') as common_words:
    STOP_WORDS.update(set(common_words.read().lower().splitlines()))

WORDNET_LEMMATIZER = WordNetLemmatizer()
PORTER_STEMMER = PorterStemmer()

def tokenize(text, lower=True):
    tokens = []
    for char in PONCTUATION:
        text = text.replace(char, ' ')
    tokens = [t if not lower else t.lower() for t in nltk.word_tokenize(text)]
    return [t for t in tokens if t.lower() not in STOP_WORDS]

def lemmatize(tokens):
    lemmatized_tokens = {}
    for token in tokens:
        term = PORTER_STEMMER.stem(WORDNET_LEMMATIZER.lemmatize(token))
        if term not in lemmatized_tokens:
            lemmatized_tokens[term] = 1
        else:
            lemmatized_tokens[term] += 1
    return list(lemmatized_tokens.items())

def process(text, terms_only=False):
    terms = lemmatize(tokenize(text))
    if terms_only:
        terms = sorted([term for term, _ in terms])
    return terms