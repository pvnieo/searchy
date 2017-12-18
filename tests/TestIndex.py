import unittest
import os
import os.path
from Document import Document
from Index import Index


class TestIndex(unittest.TestCase):

    def test_parse_cacm(self):
        index = Index.index_all(Document.parse_cacm(os.path.join(os.getcwd(), 'tests', 'cacm.all')))

        self.assertIn('programming', index.terms_idx)
        idx = index.terms_idx['programming']
        self.assertIn(11, index.terms_doc[idx])
        self.assertIn(13, index.terms_doc[idx])
        self.assertIn(14, index.terms_doc[idx])
        self.assertTrue(index.terms_doc[idx][0] < index.terms_doc[idx][1])
        self.assertTrue(index.terms_doc[idx][1] < index.terms_doc[idx][2])

        self.assertIn('communication', index.terms_idx)
        idx = index.terms_idx['communication']
        self.assertEqual(2, len(index.terms_doc[idx]))
        
if __name__ == '__main__':
    unittest.main()
