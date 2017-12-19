
import unittest
import os
import os.path
from search.bool import BooleanSearchEngine
from Index import Index


class TestBooleanSearchEngine(unittest.TestCase):

    def test_search(self):
        index = Index.index_cacm_file(os.path.join(os.getcwd(), 'tests', 'cacm.all'), verbose=False, use_cache=False)
        engine = BooleanSearchEngine(index)

        res = engine.search('programming')
        self.assertEqual(3, len(res))
        self.assertIn(11, res)
        self.assertIn(13, res)
        self.assertIn(14, res)
        
        res = engine.search('programming & communication')
        self.assertEqual(2, len(res))
        self.assertIn(11, res)
        self.assertIn(14, res)

        res = engine.search('programming&~Communication')
        self.assertEqual(1, len(res))
        self.assertIn(13, res)

        res = engine.search('programming&~Communication')
        self.assertEqual(1, len(res))
        self.assertIn(13, res)

        res = engine.search('~communication')
        self.assertEqual(3, len(res))
        self.assertIn(12, res)
        self.assertIn(13, res)
        self.assertIn(15, res)

        res = engine.search('language&~language')
        self.assertEqual(0, len(res))
        
        res = engine.search('machines|computer')
        self.assertEqual(3, len(res))
        self.assertIn(11, res)
        self.assertIn(13, res)
        self.assertIn(14, res)

if __name__ == '__main__':
    unittest.main()
