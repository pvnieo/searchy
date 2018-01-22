# stdlib
import math
import numpy as np


# ----------------------------
#      Weighting methods
# ----------------------------

def frequency_weighting(inversed_index, docs_idx, terms):
    """
    w[d][t] = tf
    :param inversed_index: inversed index
    :param docs_idx: documents index
    :param terms: list of terms to weight
    :returns: weights dict { doc_id => [ w_term_0, w_term_1 ... ] }
    """
    weights = {}
    len_terms = len(terms)
    for i, term in enumerate(terms):
        for doc_id, tf in inversed_index[term].items():
            if doc_id not in weights:
                weights[doc_id] = np.zeros(len_terms)
            weights[doc_id][i] = tf
    return weights

def tfidf_weighting(inversed_index, docs_idx, terms):
    """
    w[d][t] = (1 / sqrt(sum(w[d][t] for t in terms))) * (1 + log(tf)) / (1 + log(moy_tf(d))) * log(N / dft)
    :param inversed_index: inversed index
    :param docs_idx: documents index
    :param terms: list of terms to weight
    :returns: weights dict { doc_id => [ w_term_0, w_term_1 ... ] }
    """
    weights = {}
    len_terms = len(terms)
    total_terms = len(inversed_index)
    for i, term in enumerate(terms):
        len_posting = len(inversed_index[term])
        for doc_id, tf in inversed_index[term].items():
            if doc_id not in weights:
                weights[doc_id] = np.zeros(len_terms)
            weights[doc_id][i] = (1 + math.log(tf)) * math.log(total_terms / len_posting, 10)
    for doc_id in weights:
        doc_w_sum = sum(weights[doc_id])
        doc = docs_idx[doc_id]
        for i in range(len_terms):
            weights[doc_id][i] *= (1 / math.sqrt(doc_w_sum)) * (1 / (1 + math.log(doc.m_freq)))
    return weights

def nf_weighting(inversed_index, docs_idx, terms):
    """
    w[t][d] = tf / max(tf in d)
    :param inversed_index: inversed index
    :param docs_idx: documents index
    :param terms: list of terms to weight
    :returns: weights dict { doc_id => [ w_term_0, w_term_1 ... ] }
    """
    weights = {}
    len_terms = len(terms)
    for i, term in enumerate(terms):
        for doc_id, tf in inversed_index[term].items():
            doc = docs_idx[doc_id]
            if doc_id not in weights:
                weights[doc_id] = np.zeros(len_terms)
            weights[doc_id][i] = tf / doc.max_freq
    return weights

WEIGHTINGS = {
    'f': frequency_weighting,
    'tfidf': tfidf_weighting,
    'nf': nf_weighting
}


# ------------------------
#      Norms methods
# ------------------------

def cos_norm(q, d):
    prod = sum(np.multiply(q, d))
    norm_d = sum([x**2 for x in d])
    norm_q = sum([x**2 for x in q])
    return prod / (math.sqrt(norm_q) * math.sqrt(norm_d))

def dice_norm(q, d):
    mult = sum(np.multiply(q, d))
    return 2 * mult / (sum(q) + sum(d))

def jaccard_norm(q, d):
    mult = sum(np.multiply(q, d))
    den = sum(q) + sum(d) - mult
    if den == 0:
        return 0 
    return mult / den

def overlap_norm(q, d):
    mult = sum(np.multiply(q, d))
    return mult / (min(sum(q), sum(d)))

NORMS = {
    'cos': cos_norm,
    'dice': dice_norm,
    'jaccard': jaccard_norm,
    'overlap': overlap_norm
}
