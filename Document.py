# stdlib
import os
import os.path
# project
import words
from utils import COLOR, replace_i, hash_collection, get_cache, set_cache


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
		terms_count = 0
		with open(filepath, 'r') as cacm_file:
			for line in cacm_file:
				line = line.rstrip()
				parts = line.split()
				if parts[0] == '.I':
					if curr is not None:
						terms_count += len(curr.terms)
						docs.append(curr)
					curr = Document(title="["+parts[1]+"] ")
				elif parts[0] in wanted_markers:
					curr.add_content_line(line)
					title = False
					if parts[0] == '.T':
						title = True
					recording = True
				elif parts[0] in ignored_markers:
					recording = False
					title = False
				elif not parts[0].startswith('.') and recording:
					if title:
						curr.add_title_line(line)
					curr.add_content_line(line)
					curr.process_content(line)
		if curr is not None:
			terms_count += len(curr.terms)
			docs.append(curr)
		if verbose:
			print("Loaded {}".format(filepath))
			print("  documents \t {}".format(len(docs)))
			print("  terms \t {}".format(terms_count))
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
		terms_count = 0
		for root, _, files in os.walk(dirpath):
			for filename in files:
				filepath = os.path.join(root, filename)
				doc = Document(title=filepath, url=filepath)
				with open(filepath, 'r') as opened:
					doc.process_content(opened.read())
					if hold_content:
						doc.content = opened.read()
				terms_count += len(doc.terms)
				docs.append(doc)

		if verbose:
			print("Loaded {}".format(dirpath))
			print("  documents \t {}".format(len(docs)))
			print("  terms \t {}".format(terms_count))
		if use_cache:
			set_cache(cachedname, docs)

		return docs

	def __init__(self, title=None, url=None, content=None):
		self.title = title
		self.content = content
		self.url = url
		self._id = None
		self.terms = None
		self.len_terms = 0

	def add_content_line(self, line):
		if self.content is not None:
			self.content += "\n" + line
		else:
			self.content = line

	def add_title_line(self, line):
		if self.title is not None:
			self.title += "\n" + line
		else:
			self.title = line

	def set_id(self, doc_id):
		self._id = doc_id

	def get_id(self):
		return self._id

	def highlighted_content(self, query, color=COLOR.BOLD):
		content = self.content
		if (content is None) and (self.url is not None):
			with open(self.url, 'r') as opened:
				content = opened.read()
		elif content is None and self.url is None:
			return ""
		query = query.replace('&', ' ')
		query = query.replace('|', ' ')
		query = query.replace('~', ' ')
		for term, _ in words.process(query):
			replacement = "{}{}{}".format(color, term, COLOR.ENDC)
			content = replace_i(content, term, replacement)
		return content

	def get_terms(self):
		return self.terms

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
		return self.terms
