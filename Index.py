# project
from Document import Document
from utils import insert_sorted, hash_collection, get_cache, set_cache


class Index:

    @staticmethod
    def index_all(docs, cache_name=None, use_cache=True, overwrite_cache=False):        
        if use_cache and not overwrite_cache:
            cached = get_cache(cache_name)
            if cached is not None:
                return cached
        index = Index()
        for doc in docs:
            index.add_doc(doc)
        if use_cache:
            set_cache(cache_name, index)
        return index

    @staticmethod
    def index_cacm_file(filepath, verbose=True, use_cache=True, overwrite_cache=False):
        cache_name = hash_collection(filepath) + '.index.bin'
        docs = Document.parse_cacm(filepath, verbose, use_cache, overwrite_cache)
        index = Index.index_all(docs, cache_name, use_cache, overwrite_cache)
        return index

    @staticmethod
    def index_directory(dirpath, verbose=True, use_cache=True, overwrite_cache=False, hold_content=False, buffer_size=5000):
        cache_name = hash_collection(dirpath) + '.index.bin'
        docs = Document.read_dir(dirpath, verbose, use_cache, overwrite_cache, hold_content)
        index = Index.index_all(docs, cache_name, use_cache, overwrite_cache)
        return index

    def __init__(self):
        # term_id => term
        self.terms_idx = {}
        self.terms_rev_idx = {}
        # doc_id => document object
        self.docs_idx = {}
        self.matrix = []
        
    def get_term_id(self, term):
        if term in self.terms_rev_idx:
            return self.terms_rev_idx[term]
        term_id = len(self.matrix)
        self.matrix.append([])
        self.terms_rev_idx[term] = term_id
        self.terms_idx[term_id] = term
        return term_id

    def get_term_by_id(self, term_id):
        return self.terms_idx[term_id]

    def get_doc_by_id(self, doc_id):
        return self.docs_idx[doc_id]

    def add_doc(self, doc):
        self.docs_idx[doc.identifier] = doc
        for term in doc.tokens:
            id_term = self.get_term_id(term)
            insert_sorted(self.matrix[id_term], doc.identifier)
