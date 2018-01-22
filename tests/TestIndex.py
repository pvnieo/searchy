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

        self.assertIn('program', index.inversed_index)
        self.assertIn(11, index.inversed_index['program'])
        self.assertIn(13, index.inversed_index['program'])
        self.assertIn(14, index.inversed_index['program'])

        self.assertIn('commun', index.inversed_index)
        self.assertEqual(2, len(index.inversed_index['commun']))
        
if __name__ == '__main__':
    unittest.main()
