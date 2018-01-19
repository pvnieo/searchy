import unittest
import warnings
import os
import os.path
from Document import Document
from Index import Index


class TestIndex(unittest.TestCase):

    def test_parse_cacm(self):
        warnings.simplefilter("ignore")
        index = Index.index_cacm_file(os.path.join(os.getcwd(), 'tests', 'cacm.all'), verbose=False, use_cache=False)

        self.assertIn('program', index.terms_rev_idx)
        term_id = index.terms_rev_idx['program']
        self.assertIn(0, [doc_id for doc_id, _ in index.inversed_index[term_id]])
        self.assertIn(2, [doc_id for doc_id, _ in index.inversed_index[term_id]])
        self.assertIn(3, [doc_id for doc_id, _ in index.inversed_index[term_id]])
        self.assertTrue(index.inversed_index[term_id][0][0] < index.inversed_index[term_id][1][0])
        self.assertTrue(index.inversed_index[term_id][1][0] < index.inversed_index[term_id][2][0])

        self.assertIn('commun', index.terms_rev_idx)
        term_id = index.terms_rev_idx['commun']
        self.assertEqual(2, len(index.inversed_index[term_id]))
        
if __name__ == '__main__':
    unittest.main()
