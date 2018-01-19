# stdlib
import math
# 3p
from sortedcontainers import SortedList
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
        index.get_tf_idf_weights(verbose=verbose)
        index.get_normalized_frequency_weights(verbose=verbose)
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

    @staticmethod
    def tf_idf_weighting(inversed_index, n):
        """
        :param inversed_index: inversed index
        :param N: total number of documents
        :returns: weight matrix with rows:
                  (w_doc_0 | w_doc_1 | ... | w_doc_n) for each term_id
        """
        weight = []
        for term_id, posting_list in enumerate(inversed_index):
            weight.append([0]*n)
            for doc_id, tf in posting_list:
                weight[term_id][doc_id] = (1 + math.log(tf, 10)) * math.log(n / len(posting_list), 10)
        return weight

    @staticmethod
    def normalized_frequency_weighting(inversed_index, n):
        """
        :param inversed_index: inversed index
        :param n: total number of documents
        :returns: normalized frequency matrix with rows:
                  (w_doc_0 | w_doc_1 | ... | w_doc_n) for each term_id
        """
        weight = []
        max_tf_for_doc = {}
        for term_id, posting_list in enumerate(inversed_index):
            weight.append([0]*n)
            for doc_id, tf in posting_list:
                if doc_id not in max_tf_for_doc:
                    max_tf_for_doc[doc_id] = Index.max_tf_for_doc(inversed_index, doc_id)
                weight[term_id][doc_id] = tf / max_tf_for_doc[doc_id]
        return weight

    @staticmethod
    def max_tf_for_doc(inversed_index, doc_id):
        """
        :param inversed_index: inversed index
        :param doc_id: document id
        :returns: maximum term frequency in document 
        """
        max_tf = 0
        for posting_list in inversed_index:
            for _doc_id, tf in posting_list:
                if _doc_id == doc_id: 
                    max_tf = max(max_tf, tf)
        return max_tf

    def __init__(self):
        self.inversed_index = []

        # term_id => term
        self.terms_idx = []
        # term => term_id
        self.terms_rev_idx = {}
        # doc_id = document object
        self.docs_idx = []
        
        self._tf_idf_weights = None
        self._normalized_frequency_weights = None

    def get_docs_idx(self):
        return self.docs_idx
    
    def get_terms_idx(self):
        return self.terms_idx

    def get_tf_idf_weights(self, verbose=True):
        if self._tf_idf_weights is not None:
            return self._tf_idf_weights
        if verbose: print('Calculating tf-idf weights matrix')
        self._tf_idf_weights = Index.tf_idf_weighting(self.inversed_index, len(self.docs_idx))
        return self._tf_idf_weights

    def get_normalized_frequency_weights(self, verbose=True):
        if self._normalized_frequency_weights is not None:
            return self._normalized_frequency_weights
        if verbose: print('Calculating normalized frequency weights matrix')
        self._normalized_frequency_weights = Index.normalized_frequency_weighting(self.inversed_index, len(self.docs_idx))
        return self._normalized_frequency_weights
        
    def get_term_id(self, term):
        if term in self.terms_rev_idx:
            return self.terms_rev_idx[term]
        return None

    def get_term_by_id(self, term_id):
        if 0 <= term_id < len(self.terms_idx):
            return self.terms_idx[term_id]
        return None

    def get_doc_by_id(self, doc_id):
        if 0 <= doc_id < len(self.docs_idx):
            return self.docs_idx[doc_id]
        return None

    def add_term(self, term):
        id_term = len(self.terms_idx)
        self.terms_idx.append(term)
        self.terms_rev_idx[term] = id_term
        self.inversed_index.append(SortedList())
        return id_term
    
    def add_doc(self, doc):
        doc_id = len(self.docs_idx)
        doc.set_id(doc_id)
        self.docs_idx.append(doc)
        for term, frequency in doc.get_terms():
            id_term = self.get_term_id(term)
            if id_term is None:
                id_term = self.add_term(term)
            self.inversed_index[id_term].add((doc_id, frequency))
        doc.del_terms()
        return doc_id