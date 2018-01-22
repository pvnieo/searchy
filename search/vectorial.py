# 3p
from sortedcontainers import SortedList
# project
import words
from search.calc import WEIGHTINGS, NORMS
from Document import Document


class VectorialSearchEngine:
    
    def __init__(self, index, weighting='tfidf', norm='dice', threshold=0.5):
        self.index = index

        if norm not in NORMS:
            raise Exception(f'Unkown norm: {norm}')
        self.norm = NORMS[norm]
        self.weighting = WEIGHTINGS[weighting]
        self.threshold = threshold

    # Query processing
    def process_query(self, query):
        query_doc = Document(identifier=-1, content=query)
        terms = words.process(query, terms_only=True)
        self.index.add_doc(query_doc)
        weights = self.weighting(self.index.get_inversed_index(), self.index.get_docs_idx(), terms)
        query_weights = weights[query_doc.get_id()]
        docs_weights = { doc_id: weight for doc_id, weight in weights.items() if doc_id != query_doc.get_id() }
        self.index.del_doc(query_doc.get_id(), terms)
        return query_weights, docs_weights

    # Vectorial Search
    def search(self, query, top=10):
        results = SortedList()
        total = 0
        query_weights, docs_weights = self.process_query(query)
        for doc_id, document_weights in docs_weights.items():
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
