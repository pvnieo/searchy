from math import *
import numpy as np

class WeightingCalculation:

    @staticmethod
    def tf_idf_weighting(inversed_index, N):
        # N = nombre de documents 
        w = []
        for term_id, posting_list in enumerate(inversed_index):
            w.append([])
            for i in range(N+1):
                w[term_id].append(0)
            for tupl in posting_list:
                w[term_id][tupl[0]] = (1 + log(tupl[1],10)) * log(N/len(posting_list),10)
            # w est une matrice, les lignes sont les tokens, et les colonnes sont les documents, l'intersection est le document
        return w

    @staticmethod
    def normalized_frequency_weighting(inversed_index):
        w = []
        max_tf_for_doc_list = []
        for term_id, posting_list in enumerate(inversed_index):
            w.append([])
            for i in range(N+1):
                w[term_id].append(0)
                max_tf_for_doc_list.append(0)
            for doc_id, tupl in enumerate(posting_list):
                max_for_doc = max_tf_for_doc_list(doc_id) if max_tf_for_doc_list(doc_id) != 0 else compute_max_tf_for_doc(inversed_index,max_tf_for_doc_list, doc_id)
                w[term_id][doc_id] = tupl[1]/max_for_doc
        return w



def max_tf_for_doc(inversed_index, liste, id_doc):
    max_tf = 0
    for posting_list in inversed_index:
        for tupl in posting_list:
            if tupl[0] <= id_doc and tupl[0] == id_doc:
                if tupl[1] > max_tf:
                    max_tf = tupl[1]
                break
            elif tupl[0] > id_doc:
                break
    liste[id_doc] = max_tf
    return max_tf

