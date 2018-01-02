# stdlib
import os
import os.path
# 3p
import nltk
# project
from utils import COLOR, replace_i, hash_collection, get_cache, set_cache


STOP_WORDS = set(nltk.corpus.stopwords.words('english'))
PONCTUATION = set(['.', ',', ':', ';', ')', '(', '[', ']', ' ', '{', '}', '"', '-', '/', '\\'])
with open("Data/CACM/common_words", 'r') as common_words:
	STOP_WORDS.update(set(common_words.read().lower().splitlines()))

class Document:
	LAST_ID = 0

	@staticmethod
	def parse_cacm(filepath, verbose=False, use_cache=True, overwrite_cache=False):
		cachedname = hash_collection(filepath) + '.docs.bin'
		if use_cache and (not overwrite_cache):
			cached = get_cache(cachedname)
			if cached is not None:
				return cached
		if verbose:
			print("Loading {}".format(filepath))

		ignored_markers = ['.B', '.A', '.N', '.X']
		wanted_markers = ['.T', '.W', '.K']

		docs = []
		curr = None
		recording = False
		title = False
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
					curr.add_content_line(line.rstrip())
					title = False
					if parts[0] == '.T':
						title = True
					recording = True
				elif parts[0] in ignored_markers:
					recording = False
					title = False
				elif not parts[0].startswith('.') and recording:
					if title:
						curr.add_title_line(line.rstrip())
					curr.add_content_line(line.rstrip())
					curr.tokenize(line)
		if curr is not None:
			token_count += len(curr.tokens)
			docs.append(curr)

		if verbose:
			print("Loaded {}".format(filepath))
			print("  documents \t {}".format(len(docs)))
			print("  tokens \t {}".format(token_count))
		if use_cache:
			set_cache(cachedname, docs)

		return docs

	@staticmethod
	def read_dir(dirpath, verbose=False, use_cache=True, overwrite_cache=False, hold_content=False):
		cachedname = hash_collection(dirpath) + '.docs.bin'
		if use_cache and (not overwrite_cache):
			cached = get_cache(cachedname)
			if cached is not None:
				return cached

		if verbose:
			print("Loading {}".format(dirpath))
		docs = []
		token_count = 0
		for root, _, files in os.walk(dirpath):
			for filename in files:
				filepath = os.path.join(root, filename)
				doc = Document(title=filepath)
				with open(filepath, 'r') as opened:
					doc.tokenize(opened.read())
					if hold_content:
						doc.content = opened.read()
				token_count += len(doc.tokens)
				docs.append(doc)

		if verbose:
			print("Loaded {}".format(dirpath))
			print("  documents \t {}".format(len(docs)))
			print("  tokens \t {}".format(token_count))
		if use_cache:
			set_cache(cachedname, docs)

		return docs

	def __init__(self, identifier=None, title=None, content=None):
		self.identifier = identifier or self.get_new_id()
		self.title = title or ""
		self.content = content or ""
		self.tokens = []
		self.tokenizer = nltk.word_tokenize
		self.tokenize(self.content)

	def add_content_line(self, line):
		if len(self.content) > 0:
			self.content += "\n" + line
		else:
			self.content = line

	def add_title_line(self, line):
		if len(self.title) > 0:
			self.title += "\n" + line
		else:
			self.title = line

	def get_new_id(self):
		Document.LAST_ID += 1
		return Document.LAST_ID

	def highlight(self, term, color=COLOR.BOLD):
		replacement = "{}{}{}".format(color, term, COLOR.ENDC)
		self.content = replace_i(self.content, term, replacement)

	def reset_highlighted(self):
		self.content = self.content.replace(COLOR.BOLD, "")
		self.content = self.content.replace(COLOR.ENDC, "")

	def tokenize(self, text):
		for char in PONCTUATION:
			text = text.replace(char, ' ')
		for token in [t.lower() for t in self.tokenizer(text)]:
			if token in STOP_WORDS:
				continue
			self.tokens.append(token)
