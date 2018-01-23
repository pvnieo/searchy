# stdlib
from time import time
import sys
import os.path
from copy import deepcopy
# project
from Document import Document
from utils import hash_collection, get_cache, set_cache


class Index:

    @staticmethod
    def print_stats(index, spent=0):
        memory = sys.getsizeof(index.inversed_index)
        memory += sys.getsizeof(index.docs_idx)
        print("  documents \t {}".format(len(index.docs_idx)))
        print("  terms \t {}".format(len(index.inversed_index)))
        spent_str = '' if spent == 0 else 'time: {:.2f} s     '.format(spent)
        print(spent_str + 'memory: {:.2f} mb'.format(memory / (1024**2)))

    @staticmethod
    def index_cacm_file(filepath, verbose=True, use_cache=True, overwrite_cache=False):
        start = time()
        if verbose:
            print("Loading {}".format(filepath))
        cache_name = hash_collection(filepath) + '.index.bin'
        if use_cache and not overwrite_cache:
            cached = get_cache(cache_name)
            if cached is not None:
                if verbose:
                    print(f'Using cache {cache_name[:8]}')
                    Index.print_stats(cached)
                return cached
        index = Index()
        for doc in Document.parse_cacm(filepath):
            index.add_doc(doc)
        if use_cache:
            set_cache(cache_name, index)
        
        end = time()
        if verbose:
            print("Loaded {}".format(filepath))
            Index.print_stats(index, end-start)
        return index

    @staticmethod
    def index_directory(dirpath, verbose=True, use_cache=True, overwrite_cache=False, hold_content=False):
        start = time()
        if verbose:
            print("Loading {}".format(dirpath))
        
        index = None
        for root, _, files in os.walk(dirpath):
            total = len(files)
            if total == 0: continue
            count = 1
            cache_name = hash_collection(root) + '.index.bin'
            if use_cache and not overwrite_cache:
                cached = get_cache(cache_name)
                if cached is not None:
                    if verbose: print(f' Using cache {cache_name[:8]}')
                    if index is None:
                        index = cached
                    else:
                        index.extend(cached)
                    continue
            new_index = Index()
            for filename in files:
                filepath = os.path.join(root, filename)
                doc = Document(title=filepath, url=filepath)
                with open(filepath, 'r') as opened:
                    doc.process_content(opened.read())
                    if hold_content:
                        doc.content = opened.read()
                new_index.add_doc(doc)
                if verbose: print(" Indexing {} {:8.2f}%".format(root, count * 100 / total), end='\r')
                count += 1
            if verbose: print()

            if use_cache:
                set_cache(cache_name, new_index)
            if index is None:
                index = new_index
            else:
                index.extend(new_index)
        
        end = time()
        memory = sys.getsizeof(index.inversed_index)
        memory += sys.getsizeof(index.docs_idx)
        if verbose:
            print("Loaded {}".format(dirpath))
            Index.print_stats(index, end-start)
        return index

    def __init__(self):
        self.inversed_index = {}
        self.docs_idx = {}

    def extend(self, index):
        for term in index.inversed_index:
            if term not in self.inversed_index:
                self.inversed_index[term] = deepcopy(index.inversed_index[term])
            else:
                for doc_id, frequency in index.inversed_index[term].items():
                    if doc_id in self.inversed_index[term]:
                        self.inversed_index[term][doc_id] += frequency
                    else:
                        self.inversed_index[term][doc_id] = frequency
        for doc_id, doc in index.docs_idx.items():
            if doc_id not in self.docs_idx:
                self.docs_idx[doc_id] = doc

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
