import unittest
import os
import os.path
from Document import Document
from Index import Index


class TestIndex(unittest.TestCase):

    def test_parse_cacm(self):
        index = Index.index_cacm_file(os.path.join(os.getcwd(), 'tests', 'cacm.all'), verbose=False, use_cache=False)

        self.assertIn('programming', index.terms_rev_idx)
        idx = index.terms_rev_idx['programming']
        self.assertIn(11, index.matrix[idx])
        self.assertIn(13, index.matrix[idx])
        self.assertIn(14, index.matrix[idx])
        self.assertTrue(index.matrix[idx][0] < index.matrix[idx][1])
        self.assertTrue(index.matrix[idx][1] < index.matrix[idx][2])

        self.assertIn('communication', index.terms_rev_idx)
        idx = index.terms_rev_idx['communication']
        self.assertEqual(2, len(index.matrix[idx]))
        
if __name__ == '__main__':
    unittest.main()
