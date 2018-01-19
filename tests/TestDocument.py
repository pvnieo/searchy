import unittest
import warnings
import os
import os.path
from Document import Document


class TestDocument(unittest.TestCase):

    def test_parse_cacm(self):
        warnings.simplefilter("ignore")
        documents = Document.parse_cacm(os.path.join(os.getcwd(), 'tests', 'cacm.all'), verbose=False, use_cache=False)

        self.assertEqual(len(documents), 5)

        self.assertIn('program', [term for term, _ in documents[0].terms])
        self.assertIn('commun', [term for term, _ in documents[0].terms])
        self.assertIn('recurs', [term for term, _ in documents[4].terms])

        self.assertNotIn(' ', documents[0].terms)

if __name__ == '__main__':
    unittest.main()
