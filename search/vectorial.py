# stdlib
import math
# 3p
import numpy as np
from sortedcontainers import SortedList
# project
import words


# Weightings methods
def tfidf_weighting(index, query, epsilon=0.5):
    frequency = dict(words.process(query))
    len_docs = len(index.get_docs_idx())
    len_terms = len(index.get_terms_idx())
    query_weights = [0]*len_terms
    for term_id in range(len_terms):
        tf = 0
        term = index.get_term_by_id(term_id)
        if term is not None and term in frequency:
            tf = frequency[term]
        if tf > 0:
            query_weights[term_id] = (1 + math.log(tf, 10)) * math.log((len_docs / len(index.inversed_index[term_id])), 10)
        else:
            query_weights[term_id] = 0
    return np.array(query_weights)

def nf_weighting(index, query):
    frequency = dict(words.process(query))
    len_docs = len(index.get_docs_idx())
    len_terms = len(index.get_terms_idx())
    query_weights = [0]*len_terms
    for term_id in range(len_terms):
        tf = 0
        term = index.get_term_by_id(term_id)
        if term is not None and term in frequency:
            tf = frequency[term]
        query_weights[term_id] = tf
    # max_frequency = max(query_weights)
    # query_weights = [w / max_frequency for w in query_weights]
    return np.array(query_weights)

# Norms Definitions
def cos_norm(q, d):
    prod = sum(np.multiply(np.array(q), np.array(d)))
    norm_d = sum([x**2 for x in d])
    norm_q = sum([x**2 for x in q])
    return prod /(math.sqrt(norm_q) * math.sqrt(norm_d))

def dice_norm(q, d):
    mult = sum(np.multiply(np.array(q), np.array(d)))
    return 2 * mult /(sum(q) + sum(d))

def jaccard_norm(q, d):
    mult = sum(np.multiply(np.array(q), np.array(d)))
    return mult /(sum(q) + sum(d) - mult)

def overlap_norm(q, d):
    mult = sum(np.multiply(np.array(q), np.array(d)))
    return mult /(min(sum(q), sum(d)))


class VectorialSearchEngine:
    
    def __init__(self, index, weighting='tfidf', norm='dice', threshold=0.5):
        self.index = index
        self.len_docs = len(self.index.get_docs_idx())
        self.len_terms = len(self.index.get_terms_idx())
        if weighting == 'tfidf':
            self.weights = np.array(self.index.get_tf_idf_weights())
        elif weighting == 'nf':
            self.weights = np.array(self.index.get_normalized_frequency_weights())
        else:
            raise Exception(f'Unkown weighting method: {weighting}')

        if norm not in VectorialSearchEngine.NORMS:
            raise Exception(f'Unkown norm: {norm}')
        self.norm = VectorialSearchEngine.NORMS[norm]
        self.weighting = VectorialSearchEngine.WEIGHTINGS[weighting]
        self.threshold = threshold

    NORMS = {
        'cos': cos_norm,
        'dice': dice_norm,
        'jaccard': jaccard_norm,
        'overlap': overlap_norm
    }

    WEIGHTINGS = {
        'tfidf': tfidf_weighting,
        'nf': nf_weighting
    }

    # Query processing
    def process_query(self, query):
        return self.weighting(self.index, query)

    # Vectorial Search
    def search(self, query, top=10):
        results = SortedList()
        total = 0
        query_weights = self.process_query(query)
        for doc_id in range(self.len_docs):
            document_weights = self.weights[:, doc_id]
            score = self.norm(query_weights, document_weights)
            if score >= self.threshold:
                total += 1
            else:
                continue
            if len(results) == top:
                if results[-1][0] > -score:
                    results.pop(-1)
                else:
                    continue
            results.add((-score, doc_id))
        return results, total

