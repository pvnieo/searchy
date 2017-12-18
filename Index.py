from collections import defaultdict


class Index:

    @staticmethod
    def index_all(docs):
        index = Index()
        for doc in docs:
            index.add_doc(doc)
        return index

    def __init__(self):
        self.terms_idx = {}
        self.rev_terms_ix = []
        self.terms_doc = defaultdict(list)

    def print(self):
        for term_id, docs in self.terms_doc.items():
            print(self.rev_terms_ix[term_id], docs)

    def add_term(self, term):
        n = len(self.terms_idx)
        if term not in self.terms_idx:
            self.terms_idx[term] = n
            self.rev_terms_ix.append(term)
        return self.terms_idx[term]

    def add_doc(self, doc):
        for term in doc.tokens:
            id_term = self.add_term(term)
            insert_sorted(self.terms_doc[id_term], doc.identifier)


def insert_sorted(array, element):
    n = len(array)
    for i in range(n):
        if element < array[i]:
            array.insert(i, element)
            return
        elif element == array[i]:
            return
    array.append(element)
