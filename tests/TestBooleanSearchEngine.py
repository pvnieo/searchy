
import unittest
import warnings
import os
import os.path
from search.bool import BooleanSearchEngine
from Index import Index


class TestBooleanSearchEngine(unittest.TestCase):

    def test_search(self):
        warnings.simplefilter("ignore")
        index = Index.index_cacm_file(os.path.join(os.getcwd(), 'tests', 'cacm.all'), verbose=False, use_cache=False)
        engine = BooleanSearchEngine(index)

        res, total = engine.search('programming')
        res = [doc_id for _, doc_id in res]
        self.assertEqual(3, total)
        self.assertIn(0, res)
        self.assertIn(2, res)
        self.assertIn(3, res)
        
        res, total = engine.search('programming & communication')
        res = [doc_id for _, doc_id in res]
        self.assertEqual(2, total)
        self.assertIn(0, res)
        self.assertIn(3, res)

        res, total = engine.search('programming&~Communication')
        res = [doc_id for _, doc_id in res]
        self.assertEqual(1, total)
        self.assertIn(2, res)

        res, total = engine.search('programming&~Communication')
        res = [doc_id for _, doc_id in res]
        self.assertEqual(1, total)
        self.assertIn(2, res)

        res, total = engine.search('~communication')
        res = [doc_id for _, doc_id in res]
        self.assertEqual(3, total)
        self.assertIn(1, res)
        self.assertIn(2, res)
        self.assertIn(4, res)

        res, total = engine.search('language&~language')
        res = [doc_id for _, doc_id in res]
        self.assertEqual(0, total)
        
        res, total = engine.search('machines|computer')
        res = [doc_id for _, doc_id in res]
        self.assertEqual(3, total)
        self.assertIn(0, res)
        self.assertIn(2, res)
        self.assertIn(3, res)

if __name__ == '__main__':
    unittest.main()
