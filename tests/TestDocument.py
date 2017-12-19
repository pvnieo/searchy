import unittest
import os
import os.path
from Document import Document


class TestDocument(unittest.TestCase):

    def test_parse_cacm(self):
        documents = Document.parse_cacm(os.path.join(os.getcwd(), 'tests', 'cacm.all'), verbose=False, use_cache=False)

        self.assertEqual(len(documents), 5)

        self.assertIn('programming', documents[0].tokens)
        self.assertIn('communication', documents[0].tokens)
        self.assertIn('recursive', documents[4].tokens)

        self.assertNotIn(' ', documents[0].tokens)

if __name__ == '__main__':
    unittest.main()
