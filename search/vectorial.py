from math import *


class VectorialSearchEngine:
    
    def __init__(self, index, weights):
        self.index = index
        self.len_doc = len(self.index.docs_idx.keys())
        self.len_tokens = len(self.index.inversed_index)
        self.w = np.array(weights)

    def cos_norm(q,d):
        prod = norm_d = norm_q = 0
        for i in range(len(q)):
            prod += q[i] * d[i]
            norm_q += q[i]**2
            norm_d += d[i]**2
        return prod /(sqrt(norm_q) * sqrt(norm_d))

    def dice_norm(q,d):

    def jaccard_norm(q,d):

    def overlap_norm(q,d):

    def vectorial_search(query):
        result = []
        for j in range(1, len_doc+1):
            # We will choose which type of norms to use in parameters
            result.append((j, cos_norm(query, w[:,j-1])))
        result.sort(key=lambda score:score[1])
        result result





            