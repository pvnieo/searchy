
import nltk
import string
from nltk.stem import WordNetLemmatizer

STOP_WORDS = set(nltk.corpus.stopwords.words('english'))
PONCTUATION = string.punctuation
with open("Data/CACM/common_words", 'r') as common_words:
    STOP_WORDS.update(set(common_words.read().lower().splitlines()))
wordnet_lemmatizer = WordNetLemmatizer()

class LinguisticTreatment:

    @staticmethod
    def tokenize(text):
        tokens = []
        for char in PONCTUATION:
            text = text.replace(char, ' ')
        for token in [t.lower() for t in nltk.word_tokenize(text)]:
            if token in STOP_WORDS:
                continue
            tokens.append(token)
        return tokens

    @staticmethod
    def lemmatize(tokens):
        lemmatized_tokens = []
        for token in tokens:
            lemmatized_token = wordnet_lemmatizer.lemmatize(token)
            if lemmatized_token not in lemmatized_tokens:
                lemmatized_tokens.append(lemmatized_token)
        return lemmatized_tokens