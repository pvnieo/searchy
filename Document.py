import nltk
from nltk.stem.snowball import EnglishStemmer


STOP_WORDS = set(nltk.corpus.stopwords.words('english'))
PONCTUATION = set(['.', ',', ':', ';', ')', '(', '[', ']', ' ', '{', '}', '"', '-', '/', '\\'])
with open("Data/CACM/common_words", 'r') as common_words:
	STOP_WORDS.update(set(common_words.read().lower().splitlines()))

class Document:

	@staticmethod
	def parse_cacm(filepath, verbose=False):
		ignored_markers = ['.B', '.A', '.N', '.X']
		wanted_markers = ['.T', '.W', '.K']

		docs = []
		curr = None
		recording = False
		token_count = 0
		with open(filepath, 'r') as cacm_file:
			for line in cacm_file:
				parts = line.split()
				if parts[0] == '.I':
					if curr is not None:
						token_count += len(curr.tokens)
						docs.append(curr)
					curr = Document(int(parts[1]))
				elif parts[0] in wanted_markers:
					recording = True
				elif parts[0] in ignored_markers:
					recording = False
				elif not parts[0].startswith('.') and recording:
					curr.tokenize(line)
		if curr is not None:
			token_count += len(curr.tokens)
			docs.append(curr)
		if verbose:
			print("Loaded {}".format(filepath))
			print("  documents \t {}".format(len(docs)))
			print("  tokens \t {}".format(token_count))
		return docs

	def __init__(self, identifier, tokens=None):
		self.identifier = identifier
		self.tokens = tokens or []
		self.tokenizer = nltk.word_tokenize
		self.stemmer = EnglishStemmer()

	def tokenize(self, text):
		for char in PONCTUATION:
			text = text.replace(char, ' ')
		for token in [t.lower() for t in nltk.word_tokenize(text)]:
			if token in STOP_WORDS:
				continue
			self.tokens.append(token)
