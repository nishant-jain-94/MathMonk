import unittest
from corpus import read_corpus

class TestCorpusExtractor(unittest.TestCase):
	def test_read_corpus(self):
		data = read_corpus('conversations.corpus', extension="csv")
		assert data != None
		data = read_corpus('mathqa.corpus', extension="csv")
		assert data != None
		data = read_corpus('math_words', extension="json")

if __name__ == '__main__':
	unittest.main()