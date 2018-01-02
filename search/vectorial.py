from math import *
import numpy as np
import time

from linguistic_treatment import LinguisticTreatment

class VectorialSearchEngine:
    
    def __init__(self, index, weights):
        self.index = index
        self.len_doc = len(self.index.docs_idx.keys())
        self.len_tokens = len(self.index.inversed_index)
        self.w = np.array(weights)

    # //////////// ======Definiton of norms====== \\\\\\\\\\\\\
    @staticmethod
    def cos_norm(q,d):
        prod = sum(np.multiply(np.array(q), np.array(d)))
        norm_d = sum([x**2 for x in d])
        norm_q = sum([x**2 for x in q])
        return prod /(sqrt(norm_q) * sqrt(norm_d))

    @staticmethod
    def dice_norm(q,d):
        mult = sum(np.multiply(np.array(q), np.array(d)))
        return 2 * mult /(sum(q) + sum(d))

    @staticmethod
    def jaccard_norm(q,d):
        mult = sum(np.multiply(np.array(q), np.array(d)))
        return mult /(sum(q) + sum(d) - mult)

    @staticmethod
    def overlap_norm(q,d):
        mult = sum(np.multiply(np.array(q), np.array(d)))
        return mult /(min(sum(q), sum(d)))

    # //////////// ======Request processing====== \\\\\\\\\\\\\
    def request_processing(self, query):
        raw_q = LinguisticTreatment.tokenize(query)
        q = []
        for i in range(self.len_tokens):
            q.append(raw_q.count(self.index.get_term_by_id(i)))
        # ici on calcule les facteurs de pondération de la requete
        # il faut repenser comment calculer la pondération de la requete
        # Q = max(q)
        # for i in range(self.len_tokens):   
        #     if False: # Ici, on va choisir quelle pondération à utiliser en fonction du choix de l'utilisateur
        #     # pour des raisons de test, on utilise tf-idf par défaut
        #         epsilon = 0.5
        #         q[i] = (1 + log(q[i] + epsilon,10)) * log((self.len_doc/len(self.index.inversed_index[i])),10)
        #     else: # fréquence normalisée
        #         q[i] = q[i] / Q
        return q

    # //////////// ======Vectorial Search====== \\\\\\\\\\\\\
    def vectorial_search(self, query):
        result = []
        q = self.request_processing(query)
        for j in range(1, self.len_doc+1):
            # The user will choose witch type of norm he wanna use, here we use dice_norm for testing
            d = self.w[:,j]
            result.append((j, self.dice_norm(q,d)))
        result.sort(key=lambda score:score[1])
        return result[::-1]
        # return np.array(result[::-1])[:,0]