# project
from Document import Document
from utils import hash_collection, get_cache, set_cache


class Index:

    @staticmethod
    def index_all(docs, cache_name=None, use_cache=True, overwrite_cache=False, verbose=True):        
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
        index = Index.index_all(docs, cache_name, use_cache, overwrite_cache, verbose)
        return index

    @staticmethod
    def index_directory(dirpath, verbose=True, use_cache=True, overwrite_cache=False, hold_content=False, buffer_size=5000):
        cache_name = hash_collection(dirpath) + '.index.bin'
        docs = Document.read_dir(dirpath, verbose, use_cache, overwrite_cache, hold_content)
        index = Index.index_all(docs, cache_name, use_cache, overwrite_cache, verbose)
        return index

    def __init__(self):
        self.inversed_index = {}
        self.docs_idx = {}

    def get_inversed_index(self):
        return self.inversed_index

    def get_docs_idx(self):
        return self.docs_idx
    
    def get_doc_by_id(self, doc_id):
        if doc_id in self.docs_idx:
            return self.docs_idx[doc_id]
        return None

    def add_term_if_not_exists(self, term):
        if term not in self.inversed_index:
            self.inversed_index[term] = {}
    
    def add_doc(self, doc):
        doc_id = doc.get_id()
        self.docs_idx[doc_id] = doc
        for term, frequency in doc.terms:
            self.add_term_if_not_exists(term)
            self.inversed_index[term][doc_id] = frequency
        doc.del_terms()
        return doc_id

    def del_doc(self, doc_id, terms):
        if doc_id in self.docs_idx:
            del self.docs_idx[doc_id]
        for term in terms:
            if doc_id in self.inversed_index[term]:
                del self.inversed_index[term][doc_id]
                if len(self.inversed_index[term]) == 0:
                    del self.inversed_index[term]
