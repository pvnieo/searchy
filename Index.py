# stdlib
import pickle
import os.path
# project
from Document import Document
from utils import insert_sorted, hash_file


class Index:

    @staticmethod
    def index_all(docs):
        index = Index()
        for doc in docs:
            index.add_doc(doc)
        return index

    @staticmethod
    def index_cacm_file(filepath, verbose=True, use_cache=True):
        cachepath = os.path.join('__cache__', hash_file(filepath) + '.index.bin')
        if use_cache and os.path.exists(cachepath):
            with open(cachepath, 'rb') as cache:
                try:
                    return pickle.load(cache)
                except pickle.UnpicklingError:
                    pass
        docs = Document.parse_cacm(filepath, verbose, use_cache)
        index = Index.index_all(docs)
        if use_cache:
            with open(cachepath, 'wb') as cache:
                pickle.dump(index, cache)
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
