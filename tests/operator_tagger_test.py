import unittest
import re
from operator_tagger import OperatorTagger

class TestOperatorTagger(unittest.TestCase):
	def test_operator_tagger(self):
		operator_tagger = OperatorTagger()
		sentence = "What is 2+3?"
		tokenized_words = re.findall(r"(\b\w*[\.]?\w+\b|[\(\)\+\*\-\/])", sentence)
		expected_tagged_words = [("What", "WP"), ("is", "VBZ"), ("2", "CD"), ("+", "OPERATOR"), ("3", "CD")]
		tagged_words = operator_tagger.tag(tokenized_words)
		assert isinstance(tagged_words, list)
		assert tagged_words == expected_tagged_words

if __name__ == "__main__":
	unittest.main()
