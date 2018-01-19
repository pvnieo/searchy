# project
import words


class BooleanSearchEngine:
    def __init__(self, index):
        self.index = index
        self.interpreter = {
            '': self.contains,
            '~': self.not_contains,
            '&': self.intersect,
            '|': self.union
        }

    def contains(self, res, term):
        term = words.process(term)[0][0]
        index = self.index
        term_id = index.get_term_id(term)
        contain_doc_ids = set()
        if term_id is not None:
            contain_doc_ids = set([doc_id for (doc_id, _) in index.inversed_index[term_id]])
        return res.intersection(contain_doc_ids)

    def not_contains(self, res, docs):
        return res.difference(docs)

    def intersect(self, docs1, docs2):
        return docs1.intersection(docs2)

    def union(self, docs1, docs2):
        return docs1.union(docs2)

    def search(self, query):
        tree = EvalTree.construct_tree(query)
        res = tree.eval(self.interpreter, set(range(len(self.index.get_docs_idx()))))
        return [(1, doc_id) for doc_id in res], len(res)


class NotValidQueryExpression(Exception): pass

class EvalTree:
    OPERATORS_2 = ['&', '|']
    OPERATORS_1 = ['~']

    @staticmethod
    def is_valid(expression):
        if not expression:
            return False
        balanced = 0
        n = len(expression)
        for i, char in enumerate(expression):
            if char == '(':
                balanced += 1
            elif char == ')':
                if balanced == 0:
                    return False
                balanced -= 1
            elif char in EvalTree.OPERATORS_1:
                if i == n-1:
                    return False
                if expression[i+1] in EvalTree.OPERATORS_2:
                    return False
            elif char in EvalTree.OPERATORS_2:
                if i == n-1 or i == 0:
                    return False
                if expression[i-1] in EvalTree.OPERATORS_2:
                    return False
                if expression[i+1] in EvalTree.OPERATORS_2:
                    return False
        return balanced == 0

    @staticmethod
    def construct_tree(expression):
        # remove all whitespace characters
        expression = ''.join(expression.split())
        # check if expression is valid
        if not EvalTree.is_valid(expression):
            raise NotValidQueryExpression("Invalid query format %s" % expression)
        return EvalTree._construct_tree_rec(expression)

    @staticmethod
    def _construct_tree_rec(expression):
        if expression == '':
            return None
        if expression[0] == '(':
            balance = 1
            for i, char in enumerate(expression[1:]):
                i += 1
                if char == '(':
                    balance += 1
                elif char == ')':
                    balance -= 1
                if balance == 0:
                    if i == len(expression)-1:
                        return EvalTree._construct_tree_rec(expression[1:i])
                    else:
                        return EvalTree(expression[i+1],
                                EvalTree._construct_tree_rec(expression[1:i]),
                                EvalTree._construct_tree_rec(expression[i+2:]))
        if expression[0] in EvalTree.OPERATORS_1:
            return EvalTree(expression[0], EvalTree._construct_tree_rec(expression[1:]))
        for i, char in enumerate(expression):
            if char in EvalTree.OPERATORS_2:
                return EvalTree(expression[i], EvalTree._construct_tree_rec(expression[:i]),
                                               EvalTree._construct_tree_rec(expression[i+1:]))
        return EvalTree(expression)

    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def __str__(self, depth=0):
        ret = ""
        if self.right != None:
            ret += self.right.__str__(depth + 1)
        ret += "\n" + ("    "*depth) + str(self.data)
        if self.left != None:
            ret += self.left.__str__(depth + 1)
        return ret

    def eval(self, interpreter, results=set()):
        if self.data in EvalTree.OPERATORS_2:
            results = interpreter[self.data](self.left.eval(interpreter, results), self.right.eval(interpreter, results))
        elif self.data in EvalTree.OPERATORS_1:
            results = interpreter[self.data](results, self.left.eval(interpreter, results))
        else:
            results = interpreter[''](results, self.data)
        return results

    def get_leafs(self):
        if self.left is None and self.right is None:
            return [self.data]
        leafs = []
        if self.left is not None:
            leafs.extend(self.left.get_leafs())
        if self.right is not None:
            leafs.extend(self.right.get_leafs())
        return leafs