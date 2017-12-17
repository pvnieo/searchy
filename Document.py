from nltk.tokenize import word_tokenize


STOP_WORDS = set()
with open("Data/CACM/common_words", 'r') as common_words:
	STOP_WORDS.update(set(common_words.read().lower().splitlines()))
STOP_WORDS.update(set(['.', ',', ':', ';', ')', '(', '[', ']', ' ', '{', '}']))


class Document:

	@staticmethod
	def parse_cacm(filepath):
		ignored_markers = ['.B', '.A', '.N', '.X']
		wanted_markers = ['.T', '.W', '.K']

		docs = []
		curr = None
		recording = False
		with open(filepath, 'r') as cacm_file:
			for line in cacm_file:
				parts = line.split()
				if parts[0] == '.I':
					if curr is not None:
						docs.append(curr)
					curr = Document(int(parts[1]))
				elif parts[0] in wanted_markers:
					recording = True
				elif parts[0] in ignored_markers:
					recording = False
				elif not parts[0].startswith('.') and recording:
					curr.tokenize(line)
		if curr is not None:
			docs.append(curr)
		return docs

	def __init__(self, identifier, tokens=None):
		self.identifier = identifier
		self.tokens = tokens or []

	def tokenize(self, text):
		words = word_tokenize(text.lower())
		self.tokens.extend([token for token in words if token not in STOP_WORDS])
