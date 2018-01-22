# stdlib
import os
import os.path
# project
import words
from utils import hash_collection, get_cache, set_cache, add_line_str


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
		with open(filepath, 'r') as cacm_file:
			for line in cacm_file:
				line = line.rstrip()
				if len(line) == 0: 
					continue
				parts = line.split()
				if parts[0] == '.I':
					if curr is not None:
						docs.append(curr)
					curr = Document(identifier=int(parts[1]))
				elif parts[0] in wanted_markers:
					curr.content = add_line_str(curr.content, line)
					title = False
					if parts[0] == '.T':
						title = True
					recording = True
				elif parts[0] in ignored_markers:
					recording = False
					title = False
				elif not parts[0].startswith('.') and recording:
					if title:
						curr.title = add_line_str(curr.title, line)
					curr.content = add_line_str(curr.content, line)
					curr.process_content(line)
		if curr is not None:
			docs.append(curr)
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
		for root, _, files in os.walk(dirpath):
			for filename in files:
				filepath = os.path.join(root, filename)
				doc = Document(title=filepath, url=filepath)
				with open(filepath, 'r') as opened:
					doc.process_content(opened.read())
					if hold_content:
						doc.content = opened.read()
				docs.append(doc)

		if use_cache:
			set_cache(cachedname, docs)

		return docs

	def __init__(self, identifier=None, title=None, url=None, content=None):
		self._id = identifier
		if identifier is None:
			self._id = Document.LAST_ID
			Document.LAST_ID += 1
		else:
			Document.LAST_ID = max(identifier, Document.LAST_ID) + 1
		
		self.title = title
		self.content = content
		self.url = url
		self.terms = None

		self.len_terms = 0
		self.m_freq = 0
		self.max_freq = 0
		self.min_freq = float('inf')

		if content is not None:
			self.process_content(content)

	def get_id(self):
		return self._id

	def del_terms(self):
		del self.terms
		self.terms = None

	def process_content(self, text):
		if self.terms is None:
			self.terms = []
		frequency = dict(self.terms)
		new_frequency = dict(words.process(text))
		for term, tf in new_frequency.items():
			if term in frequency:
				frequency[term] += tf
			else:
				frequency[term] = tf
		self.terms = list(frequency.items())
		self.len_terms = len(self.terms)
		for _, freq in self.terms:
			self.m_freq += freq / self.len_terms
			self.max_freq = max(self.max_freq, freq)
			self.min_freq = min(self.min_freq, freq)
		return self.terms
