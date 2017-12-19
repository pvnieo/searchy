# stdlib
import pickle
import os.path
# 3p
import nltk
# project
from utils import COLOR, replace_i, hash_file


STOP_WORDS = set(nltk.corpus.stopwords.words('english'))
PONCTUATION = set(['.', ',', ':', ';', ')', '(', '[', ']', ' ', '{', '}', '"', '-', '/', '\\'])
with open("Data/CACM/common_words", 'r') as common_words:
	STOP_WORDS.update(set(common_words.read().lower().splitlines()))

class Document:

	@staticmethod
	def parse_cacm(filepath, verbose=False, use_cache=True):
		cachepath = os.path.join('__cache__', hash_file(filepath) + '.docs.bin')
		if use_cache and os.path.exists(cachepath):
			with open(cachepath, 'rb') as cache:
				try:
					return pickle.load(cache)
				except pickle.UnpicklingError:
					pass

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
					curr.content.append(line.rstrip())
					recording = True
				elif parts[0] in ignored_markers:
					recording = False
				elif not parts[0].startswith('.') and recording:
					curr.content.append(line.rstrip())
					curr.tokenize(line)
		if curr is not None:
			token_count += len(curr.tokens)
			docs.append(curr)
		if verbose:
			print("Loaded {}".format(filepath))
			print("  documents \t {}".format(len(docs)))
			print("  tokens \t {}".format(token_count))
		if use_cache:
			with open(cachepath, 'wb') as cache:
				pickle.dump(docs, cache)

		return docs

	def __init__(self, identifier=None, content=None, tokens=None):
		self.identifier = identifier
		self.content = content or []
		self.tokens = tokens or []
		self.tokenizer = nltk.word_tokenize

	def highlight(self, term, color=COLOR.BOLD):
		replacement = "{}{}{}".format(color, term, COLOR.ENDC)
		for i, line in enumerate(self.content):
			self.content[i] = replace_i(line, term, replacement)

	def reset_highlighted(self):
		for i in range(len(self.content)):
			self.content[i] = self.content[i].replace(COLOR.BOLD, "")
			self.content[i] = self.content[i].replace(COLOR.ENDC, "")

	def tokenize(self, text):
		for char in PONCTUATION:
			text = text.replace(char, ' ')
		for token in [t.lower() for t in nltk.word_tokenize(text)]:
			if token in STOP_WORDS:
				continue
			self.tokens.append(token)
